function [l,outliers] = getconnectionlength(X,Y)
    n = length(X);
    connections = [];
    for i = 1:n
        d = max(X);
        for j = 1:n
            if i==j
                continue
            end
            dist = ((X(j,1)-X(i,1))^2+(Y(j,1)-Y(i,1))^2)^0.5;
            if dist < d
                d = dist;
            end
        end
        connections = [connections d];
    end
    mu = mean(connections);
    sigma = 3*std(connections);
    outliers = connections<(mu+sigma) & connections>(mu-sigma);
    connections = connections(1,outliers);
    l = max(connections);
    %find outliers in connection (differ more than 3 sigma from the mean)
    %and pass them on to main function to exclude them from analysis
end