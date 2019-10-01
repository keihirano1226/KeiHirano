function B = fitplane(XYZ)

[rows,npts] = size(XYZ);

A = [XYZ' ones(npts,1)]; % Build constraint matrix
[u d v] = svd(A,0);        % Singular value decomposition.
B = v(:,4);              % Solution is last column of v.


end


       
       