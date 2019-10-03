function edge = onEdge(X,Y,i,count,neigh,margin)
selfX = X(i,1);
selfY = Y(i,1);
if selfX < margin || selfY < margin || selfX > max(X)-margin || selfY > max(Y)-margin
    edge = 0;
    return
end
for j = 1:count
    neighX = X(neigh(1,j),1);
    neighY = Y(neigh(1,j),1);
    a = (selfY - neighY) / (selfX-neighX);
    b = selfY - a * selfX;
    s = 0;
    for k=1:count
        if k == j 
            continue 
        end
        s = s + sign(Y(neigh(1,k),1)-a*X(neigh(1,k),1)-b);    
    end
    if abs(s) == count-1
        edge = 1;
        return
    else
        edge = 0;
    end
end
