function [cluster_sizes, cluster_avg, randomness,nums] = ClusterImage(Z,k,X,Y,epsilon,minclust)
% I'd say make k~3
idx = kmeans(Z,k,'MaxIter',1000);
l = length(Z);
cluster_sizes = zeros(l,1);
cluster_avg = zeros(l,1);
nums = linspace(1,l,l).';
randomness = 0;

for i=1:k
    x = X(idx == i,1);
    y = Y(idx == i,1);
    z = Z(idx == i,1);
    coeffs = nums(idx == i,1);
    [idx2, dump] = DBSCAN([x,y],epsilon,minclust);
    sizes = [];
    avgs = [];
    for j=1:length(idx2)
        if idx2(j,1) == 0
            sizes = [sizes;1];
            avgs = [avgs;z(j,1)];
        else
            sizes = [sizes; sum(idx2 == idx2(j,1))];  
            avgs = [avgs; sum(z(idx2 == idx2(j,1),1))/sum(idx2 == idx2(j,1))]; 
        end    
    end
    cluster_sizes(coeffs,1) = sizes;
    cluster_avg(coeffs,1) = avgs;

    randomness = randomness + max(idx2) + 2*sum(dump);
    nums(idx == i,1) = idx2+max(nums)-(idx2==0)*max(nums);
end
randomness = randomness/length(Z);



