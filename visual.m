tic;
filepath = "day4box5metrics.xlsx"; 
outfolder = "day4box5metrics";
if ~exist(outfolder, 'dir')
       mkdir(outfolder)
end
[num,txt,~] = xlsread(filepath);

X = num(:,txt == "X"); 
Y = num(:,txt == "Y");
Y = max(Y)*ones(length(Y),1)- Y;
S = max(X)*max(Y);
sz = num(:,txt == "Area")/(S/200000);


for i=3:length(txt)
    f = figure('visible','off');
    I = scatter([X;0],[Y;0],[sz;0.01],[num(:,i);0],"filled"); % for all colorbars to start from zero
    %I = scatter(X,Y,sz,num(:,i),"filled"); % uncomment this for a natural range of colorbars
    axis tight;
    set(gca,'visible','off')
    colormap jet;
    c = colorbar;
    c.FontSize = 25;
    name = txt(1,i);
    print(outfolder+"/"+name{1}+".png",'-dpng')
end

toc;
