[num,txt,~] = xlsread("day4box5.xlsx");
output_name = 'day4box5tiles.csv';
X = num(:,txt == "X"); 
Y = num(:,txt == "Y");
txt = txt(1,3:end);
[connection, outliers] = getconnectionlength(X,Y);
region = connection*2;
X = X(outliers,1); 
Y = Y(outliers,1);
num = num(outliers,:);
maxX = max(X)+1;
maxY = max(Y)+1;
lengthX = 200;
lengthY = 200;
partitionX = ceil(maxX/lengthX);
partitionY = ceil(maxY/lengthY);
tls = zeros(partitionY,partitionX);
randomness = zeros(partitionY,partitionX);
maX = zeros(partitionY,partitionX);
density = zeros(partitionY,partitionX);
edge = zeros(partitionY,partitionX);
images = zeros(partitionY,partitionX);
output = zeros((partitionX)*(partitionY),length(txt)*3);
n = zeros(partitionY,partitionX);
edgeL = zeros(partitionY,partitionX);
coordsX = zeros(partitionY,partitionX);
coordsY = zeros(partitionY,partitionX);
scatterplot = zeros(length(X),1);
commaHeader = [txt;repmat({','},1,numel(txt))];
commaHeader = commaHeader(:)';
headerString2 = cell2mat(commaHeader);
for i=1:length(X)
    coord1 = ceil(X(i,1)/lengthX);
    coord2 = partitionY-ceil(Y(i,1)/lengthY)+1;
    coordsX(coord2,coord1) = coordsX(coord2,coord1)+X(i,1); 
    coordsY(coord2,coord1) = coordsY(coord2,coord1)+Y(i,1); 
    n(coord2,coord1) = n(coord2,coord1)+1; 
    images(coord2,coord1,n(coord2,coord1),1:length(txt)+2) = num(i,1:end); 
end

for i=1:partitionY
    for j=1:partitionX
        if n(i,j) < 10
            n(i,j) = 0;
            continue
        end
        edge = zeros(n(i,j),1);
        neighboors = zeros(n(i,j),118);
        neighboors_small = zeros(n(i,j),118);
        for p=1:n(i,j)
            x = images(i,j,p,1);
            y = images(i,j,p,2);
            neigh = [];
            neigh_big = [];
            for t=1:n(i,j)
                x1 = images(i,j,t,1);
                y1 = images(i,j,t,2);
                dist = ((x1-x)^2+(y1-y)^2)^0.5;
                if p~=t
                    if dist < region
                        if dist < connection
                            neigh = [neigh t];
                        end
                        neigh_big = [neigh_big t];
                    end
                end
            end
            count = length(neigh_big);
            counter = length(neigh);
            neighboors(p,1:count) = neigh_big;
            neighboors_small(p,1:counter) = neigh;
            if counter ~= 0
                edge(p,1) = onEdge(X,Y,i,count,neigh_big,10);
            else % if the ith node doesn't have any neighboors
                edge(p,1) = 0;
            end
        end
        edgeL(i,j) = sum(edge)/n(i,j);
        for k=1:length(txt)
            tls(i,j,k) = sum(images(i,j,:,k+2))/n(i,j);
            maX(i,j,k) = max(images(i,j,:,k+2));
            m = images(i,j,1:n(i,j),k+2);
            xx = images(i,j,1:n(i,j),1);
            yy = images(i,j,1:n(i,j),2);
            [~, ~,randomness(i,j,k),~] = ClusterImage(m(:),2,xx(:),yy(:),40,5);
        end
    end
end
display_num = 6; % column number to display tiling of
for i=1:length(X)
    coord1 = ceil(X(i,1)/lengthX);
    coord2 = partitionY-ceil(Y(i,1)/lengthY)+1;
    scatterplot(i,3) = tls(coord2,coord1,display_num-2);
%    scatterplot(i,4) = maX(coord2,coord1,display_num-2);
%    scatterplot(i,5) = randomness(coord2,coord1,display_num-2); 
%    uncomment these to display maximum value per tile and randomness per tile
%    substitute scatterplot(:,3) in the line below by scatterplot(:,4) or scatterplot(:,5) accordingly
end
scatter([X;0],[max(Y)*ones(length(Y),1)- Y;0],20,[scatterplot(:,3);0],"filled") 
colormap jet;
axis tight;
set(gca,'visible','off')
c = colorbar;
c.FontSize = 25;

for k=1:length(txt)
    matrix = tls(:,:,k).';
    output(:,k) = matrix(:);
    matrix = maX(:,:,k).';
    output(:,length(txt)+k) = matrix(:);
    matrix = randomness(:,:,k).';
    output(:,2*length(txt)+k) = matrix(:);
end
density = n.'/(lengthX*lengthY);
density = density(:);
edgeL = edgeL.';
edgeL = edgeL(:);
matrixX = (coordsX./n).';
matrixY = (coordsY./n).';
N = n.';
M = N(:) ~= 0;
x = matrixX(:);
y = matrixY(:);
headerString1 = 'X,Y,density,edge,';

commaHeader_max = [txt;repmat({'_max,'},1,numel(txt))];
commaHeader_max = commaHeader_max(:)';
headerString_max = cell2mat(commaHeader_max);
commaHeader_rand = [txt;repmat({'_rand,'},1,numel(txt))];
commaHeader_rand = commaHeader_rand(:)';
headerString_rand = cell2mat(commaHeader_rand);
fid = fopen(output_name,'w');
fprintf(fid,'%s\n',strcat(headerString1,headerString2,headerString_max,headerString_rand));
fclose(fid);
dlmwrite(output_name,[x(M) y(M) density(M) edgeL(M) output(M,:)],'-append');
