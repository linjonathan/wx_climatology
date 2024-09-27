function [] = run_stochastic_wind()
    load('data.mat');
    
    time_hrs = (time(1:end-1) - time(1)) / (24*60*60) / 1e9;
    
    %Calculate potential temperature from temperature and pressure
    kap = 0.2854;
    theta = (tth+273.15).*(1000./pth).^kap;
    
    %compute mixed layer height
    surftheta = mean(theta(:,1:3),2); %take average of first 3 levels (nearest to the ground) as surface theta value
    mlheight  = []; windpot = []; windlay  = [];
    stoplevBL = 25;
    for i=1:(length(time_hrs))
        plevel = 2; %start at second level
        %define BL height to be where difference in theta at given level and avg of 3 levels nearest to the ground becomes greater than 0.5
        while((plevel < stoplevBL) && ((theta(i,plevel)-surftheta(i))<0.5))
            plevel = plevel + 1;
        end
        mlheight(i) = pth(i,plevel); %get BL/ML height
        %windpot(i) = 1.00*max(squeeze(tmht(i,1:plevel,6))); %calculate wind gust potential in mixed layer (no reduction)
        %calculate BL average wind
        %phalf = [tmht(i,1,1) (tmht(i,1:plevel-1,1)+tmht(i,2:plevel,1))./2 tmht(i,plevel,1)];
        %deltap = phalf(1:end-1)-phalf(2:end); %widths of levels (delta(p))
        %windlay(i) = 1/(phalf(1)-phalf(end))*sum(squeeze(tmht(i,1:plevel,6)).*deltap); %take mean value of vert integral
    end
    
    % mlp, w10u, w10v, wth, dth, pth, tth, tnum)
    i1 = midn_idx(1);
    i2 = midn_idx(2);
    [tmax,wsyn2mmax] = Stoc2minWind(mlheight(i1:i2).', 1.9438444*w10u(i1:i2).', 1.9438444*w10v(i1:i2).', ...
                                    wth(i1:i2, :), dth(i1:i2, :), pth(i1:i2, :), tth(i1:i2, :), ...
                                    time_hrs(i1:i2));
    csvwrite('stochastic_wind.txt', wsyn2mmax);
end
