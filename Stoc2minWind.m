%STOC2MINWIND.M	
%
%Generates synthetic wind time series from wind gust distribution
%Uses RUC algorithm to calculate wind gusts
%
%Brian Tang

function [tmax,wsyn2mmax] = Stoc2minWind(mlp, w10u, w10v, wth, dth, pth, tth, tnum)

%clear all;
%load stoc.mat; %testing purposes
%d1 = datenum(now); %timing purposes

% mlp = mlheight(zmidn(1):zmidn(2)); %pressure of top of mixed layer (mb)
% w10u = 1.94384449*srfc(zmidn(1):zmidn(2),9); %10m zonal wind (knots)
% w10v = 1.94384449*srfc(zmidn(1):zmidn(2),10); %10m meridional wind (knots)
% wth = squeeze(tmht(zmidn(1):zmidn(2),:,6)); %wind time-height cross section (knots)
% dth = squeeze(tmht(zmidn(1):zmidn(2),:,5)); %wind direction time-height cross section (deg)
% pth = squeeze(tmht(zmidn(1):zmidn(2),:,1)); %pressure time-height cross section (mb)
% tth = squeeze(tmht(zmidn(1):zmidn(2),:,2)); %temperature time-height cross section (C)
% tnum = timenum(zmidn(1):zmidn(2)); %datenum

%Determine mixed layer height
wgmax = [];
for i = 1:length(tnum)
    %compute mean temperature of BL
    plevel = find(pth(i,:)==mlp(i));
    
    %initialize wind gust
    wg = sqrt(w10u(i)^2+w10v(i)^2);
    
    for j = 2:plevel
        phalf = [pth(i,1) (pth(i,1:j-1)+pth(i,2:j))./2 pth(i,j)];
        deltap = phalf(1:end-1)-phalf(2:end); %widths of levels (delta(p))
        templay = 1/(phalf(1)-phalf(end))*sum(squeeze(tth(i,1:j)).*deltap); %take mean value of vert integral
        sheight = 287*(templay+273)/9.8; %scale height
	
	%determine scaling for gust (RUC model wind gust method... use power law in future?)
	height = sheight*log(pth(i,1)/pth(i,j));
	coef = 1-(height/2000);
	coef = max(coef,0.5); %coefficient cannot drop below 0.5
	
	%determine u and v components of wind at a given level
	from = dth(i,j);
	speed = wth(i,j);
	if ((from>=0) && (from<=90)) %N to E
            angle = deg2rad(90-from); %get angle from horizontal
            speedu = -1*speed*cos(angle); %calculate the u component of the wind
            speedv = -1*speed*sin(angle); %calculate the v component of the wind
        elseif ((from>90) && (from<=180)) %E to S
            angle = deg2rad(from-90);
            speedu = -1*speed*cos(angle);
            speedv = speed*sin(angle);
        elseif ((from>180) && (from<=270)) %S to W
            angle = deg2rad(270-from);
            speedu = speed*cos(angle);
            speedv = speed*sin(angle);
        elseif ((from>270) && (from<360)) %W to N
            angle = deg2rad(from-270);
            speedu = speed*cos(angle);
            speedv = -1*speed*sin(angle);
    end
	
	%calculate difference in u and v and then multiply diff by coef and add onto 10m u and v to get gust
	deltau = speedu-w10u(i);
	deltav = speedv-w10v(i);
	
	wgu = w10u(i)+coef*(deltau); %u component of wind gust
	wgv = w10v(i)+coef*(deltav); %v component of wind gust

	wg(j) = sqrt(wgu^2+wgv^2); %wind gust for given level in BL
    end
    wgmax(i) = max(wg); %get maximum value of computed BL wind gusts
    clear wg;
end

%determine max wind index to isolate interval over which to compute synthetic wind time series
windx = (w10u.^2+w10v.^2)+wgmax'.^2;
tmaxi = find(windx==max(windx));
tmax = tnum(tmaxi(1));

samp = 5; %seconds
numts = 100; %number of time series to generate

%interpolate wind data to every minute
tdens = max(tnum(1),tmax-2/24):samp/(24*60*60):min(tnum(end),tmax+2/24);
w10dens = interp1(tnum,sqrt(w10u.^2+w10v.^2),tdens);
wgdens = interp1(tnum,wgmax,tdens);
%set std dev of normally distributed wind 
sigma = abs(wgdens-w10dens)/2.5; %set wind gust to be about 99% level (ADJUSTABLE PARAMETER)
    
%generate synthetic wind time series
T = 4*60*60/samp; %interval length
n = repmat(1:floor(T/2), [numts, 1]);
%METHOD ONE (NOT AS GOOD)
% pow = (-1/3)/atan(.5)*atan(n/T)-2/3; %vary power in order to simulate change in shape of power spectrum
% an = randn(numts,floor(T/2)).*sqrt((n.^pow)./2); %Fourier coefficients (see Wunsch class notes pg 86)
% bn = randn(numts,floor(T/2)).*sqrt((n.^pow)./2);
% stovar = .5*sum((1:floor(T/2)).^pow(1,:)); %normalization of stochastic term so that it has unit variance
%METHOD TWO (BETTER)
r = .7;
phi = -(8E1*n.^(-2))+(1.5E2*n.^(-4/5)-1.5E2*n(end).^(-4/5)+.05)+(1-r^2)./(1+r^2-2*r*cos(2*pi*n./T)); %mimics sample power spectrum
an = randn(numts,floor(T/2)).*sqrt(phi./2); %Fourier coefficients, G(0,phi)... divide by two to account for a and b
bn = randn(numts,floor(T/2)).*sqrt(phi./2);
stovar = .5*sum(phi(1,:)); %normalization of stochastic term so that it has unit variance

wsyn = NaN(numts,length(tdens));
for t=1:length(tdens)
    %synthetic time series has mean=10m wind, variance as specified by sigma above, and specified power spectrum
    %don't let wind exceed peak wind gust
    wsyn(:,t) = min(wgdens(t),(w10dens(t).*ones(numts,1))+(sigma(t).*ones(numts,1)).*(1/sqrt(stovar)).*(sum(an.*cos(2*pi.*n.*t./T),2)+sum(bn.*sin(2*pi.*n.*t./T),2)));
end

wneg = find(wsyn<0); %set negative values to 0
wsyn(wneg) = 0;

%compute 2 min max
twomin = 2*60/samp;
wsyn2m = NaN(numts,length(tdens)-twomin);
for t = 1:(length(tdens)-twomin) %take 2min moving averages
    wsyn2m(:,t) = mean(wsyn(:,t:t+twomin),2);
end
    
wsyn2mmax = max(wsyn2m,[],2); %2min max for time series

%d2 = datenum(now);
%(d2-d1)*24*60*60

%save('stoc2.mat','wsyn','tdens','w10dens','wgdens');
