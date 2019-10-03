calcmetrics("day4box5.xlsx","day4box5metrics.csv")

function calcmetrics(inputname,output_name)
    tic;
    [num,txt,~] = xlsread(inputname);
    X = num(:,txt == "X"); 
    Y = num(:,txt == "Y");
    [connection, outliers] = getconnectionlength(X,Y);
    region = connection*2;
    X = X(outliers,1); 
    Y = Y(outliers,1);
    num = num(outliers,txt ~= "X" & txt ~= "Y");
    txt = txt(:,txt ~= "X" & txt ~= "Y");
    [n,d] = size(num);
    
    avgLength = zeros(n,1);
    dens = zeros(n,1);
    edge = zeros(n,1);
    center = zeros(n,1);
    numConn = zeros(n,1);
    edgeDist = zeros(n,1);
    centerDist = zeros(n,1);
    neighboors = zeros(n,118);
    neighboors_small = zeros(n,118);
    selfOverAvg = zeros(n,d);
    avgCluster = zeros(n,d);
    clusterSize = zeros(n,d);
    rangeNeigh = zeros(n,d);
    averageNeigh = zeros(n,d);
    selfOverAvgCluster = zeros(n,d);
    for i=1:n
        x = X(i,1);
        y = Y(i,1);
        neigh_big = [];
        neigh = [];
        for j=1:n
            dist = ((X(j,1)-x)^2+(Y(j,1)-y)^2)^0.5;
            if i~=j
                if dist < region
                    if dist < connection
                        avgLength(i,1) = avgLength(i,1) + dist;
                        neigh = [neigh j];
                    end
                    neigh_big = [neigh_big j];
                end
            end
        end
        count = length(neigh_big);
        counter = length(neigh);
        neighboors(i,1:count) = neigh_big;
        neighboors_small(i,1:counter) = neigh;
        numConn(i,1) = counter;
        if counter ~= 0
            avgLength(i,1) = avgLength(i,1)/counter;
            dens(i,1) = counter/avgLength(i,1);
            edge(i,1) = onEdge(X,Y,i,count,neigh_big,100);
            for p=1:d
                selfOverAvg(i,p) = num(i,p)/mean(num(neigh,p));
                averageNeigh(i,p) = mean(num(neigh,p));
                disp(num(neigh,p))
                rangeNeigh(i,p) = max(num(neigh,p))-min(num(neigh,p)); 
            end
        else % if the ith node doesn't have any neighboors
            selfOverAvg(i,1:end) = 1;
            avgLength(i,1) = 40;
            averageNeigh(i,1:end) = num(i,1:end);
            %dens(i,1) = 0;
            edge(i,1) = 1;
        end
    end

    for i=1:d
        if i == 4 || i == 5
            continue
        end
        disp(i)
        [clusterSize(:,i), avgCluster(:,i),randomness,~] = ClusterImage(averageNeigh(:,i),3,X,Y,connection,5);
        selfOverAvgCluster(:,i) = num(:,i)./avgCluster(:,i);
    end
    min_edge_dist = 100;
    for i=1:n
        if sum(ismember(i,find(edge)))>0
            edgeDist(i,1) = 0;
        else
            edgeDist(i,1) = edgeDistance(X,Y,edge,i);
            if min_edge_dist > edgeDist(i,1)
                min_edge_dist = edgeDist(i,1);
            end
        end
    end
    max_center_dist = 1/min_edge_dist^0.25;
    for i=1:n
        if sum(ismember(i,find(edge)))>0
            centerDist(i,1) = max_center_dist;
        else
            centerDist(i,1) = 1/(edgeDist(i,1))^0.25;

        end
    end


    headerString1 = 'X,Y,numConn,density,avgLength,edge,edgeDist,centerDist,';
    commaHeader = [txt;repmat({','},1,numel(txt))];
    commaHeader = commaHeader(:)';
    headerString2 = cell2mat(commaHeader);
    commaHeader_avg = [txt;repmat({'_average_neighbor,'},1,numel(txt))];
    commaHeader_avg = commaHeader_avg(:)';
    headerString_avg = cell2mat(commaHeader_avg);
    commaHeader_overavg = [txt;repmat({'_self_value_over_avgerage_neighbor,'},1,numel(txt))];
    commaHeader_overavg = commaHeader_overavg(:)';
    headerString_overavg = cell2mat(commaHeader_overavg);
    commaHeader_clustsize = [txt;repmat({'_cluster_size,'},1,numel(txt))];
    commaHeader_clustsize = commaHeader_clustsize(:)';
    headerString_clustsize = cell2mat(commaHeader_clustsize);
    commaHeader_avgclust = [txt;repmat({'_avgerage_cluster_value,'},1,numel(txt))];
    commaHeader_avgclust = commaHeader_avgclust(:)';
    headerString_avgclust = cell2mat(commaHeader_avgclust);
    commaHeader_selfoverclust = [txt;repmat({'_self_value_over_average_cluster,'},1,numel(txt))];
    commaHeader_selfoverclust = commaHeader_selfoverclust(:)';
    headerString_selfoverclust = cell2mat(commaHeader_selfoverclust);
    commaHeader_rangeNeigh = [txt;repmat({'_neighborhood_range,'},1,numel(txt))];
    commaHeader_rangeNeigh = commaHeader_rangeNeigh(:)';
    headerString_rangeNeigh = cell2mat(commaHeader_rangeNeigh);
    fid = fopen(output_name,'w');
    fprintf(fid,'%s\n',strcat(headerString1,headerString2,headerString_avg,headerString_overavg,headerString_rangeNeigh,headerString_clustsize,headerString_avgclust,headerString_selfoverclust));
    fclose(fid);
    dlmwrite(output_name,[X Y dens.*avgLength dens avgLength edge edgeDist centerDist num averageNeigh selfOverAvg rangeNeigh clusterSize avgCluster selfOverAvgCluster],'-append');
    toc;
end