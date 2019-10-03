function dist = edgeDistance(X,Y,edge,i)
selfX = X(i,1);
selfY = Y(i,1);
distances = ((X(edge==1,1)-selfX).^2+(Y(edge==1,1)-selfY).^2).^0.5;
dist = min(distances);
