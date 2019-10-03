[num,txt,~] = xlsread("new data/day4avgneigh.xlsx");
x = num(:,txt == "X"); 
y = num(:,txt == "Y"); 
[connection, outliers] = getconnectionlength(x,y);
region = connection*2;
x = x(outliers,1); 
y = y(outliers,1);
num = num(outliers,txt ~= "X" & txt ~= "Y");
y = max(y)*ones(length(y),1)-y;
z = num(:,txt == "_778");
minz = min(z);
maxz = max(z);
S = max(x)*max(y);
sz = num(:,txt == "Area")/(S/300000);
[n,d] = size(num);
k = 2;
[idx,C,sumd] = kmeans(z,k,'MaxIter',1000);
idxs = [];
dumpsx = [];
dumpsy = [];
newx = [];
newy = [];
randomness = 0;
for i = 1:k
    [idx1, dump] = DBSCAN([x(idx == i,1),y(idx == i,1)],connection,5);
    randomness = randomness + max(idx1) + 2*sum(dump);
    if i == 1
        idxs = [idxs; idx1];
    else
        idxs = [idxs; idx1+ones(length(idx1),1).*max(idxs)];
    end
    dumpsx = [dumpsx; x(dump,1)];
    dumpsy = [dumpsy; y(dump,1)];
    newx = [newx; x(idx == i,1)];
    newy = [newy; y(idx == i,1)];
    figure
    scatter([x(idx == i,1);0;0],[y(idx == i,1);0;0],20,[z(idx == i,1);0;maxz],"filled")
    axis tight;
    set(gca,'visible','off')
    colormap jet;
    c = colorbar;
    c.FontSize = 25;
end
randomness = randomness/n; 
disp(randomness)

figure
scatter([newx;dumpsx],[newy;dumpsy],20,[idxs;zeros(length(dumpsy),1)],"filled")
axis tight;
set(gca,'visible','off')
colormap jet;
c = colorbar;
c.FontSize = 25;


