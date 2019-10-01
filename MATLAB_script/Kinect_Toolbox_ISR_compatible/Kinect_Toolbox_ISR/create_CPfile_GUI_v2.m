% Create files with corners and plane masks (CP files) for different plane poses:
mkdir('CPfiles');
imidx = imNums;
delta = 10;
offs = 20;
% GT= load('PlaneCornersInfo.mat'); %%
for N=1:Nimsvar
    
    %         hip0 = imidx;
    dfiles{N}=sprintf('%04d-d.pgm', imidx(N)-1);
    imfile=['data/' dfiles{N}];
    %     i1=imread(imfile);
    i1 = (read_disparity(imfile));
    figure(10)
    im_rgb=visualize_disparity(i1);
    imshow(im_rgb);hold on
%     keyboard
%     if ~isempty(GT.PlaneCornersInfo{imidx(N)})
%     pts = GT.PlaneCornersInfo{imidx(N)}.ptsPix;
% %     keyboard
%     scatter (pts(1,:),pts(2,:),'filled');
%     end
    %     imagesc(i1);
    %get corners of the plane:
    
    [X,Y] = ginput;
    
    for i=1:size(X,1)
        text(X(i),Y(i),num2str(i), 'Color','w','FontSize',16);
    end
    
    ch=input('Insert point coordinates? y/n     ','s');
    if ch=='y'
        clear disp ptsMM ptsPix
        disp('Insert -1 if the coordinate is unknown.');
        for i=1:size(X,1)
            str = sprintf('Point %d:',i);
            disp(str);
            x=input('x = ');
            y=input('y = ');
            ptsMM(1,i) = x;
            ptsMM(2,i) = y;
            ptsPix(1,i) = X(i);
            ptsPix(2,i) = Y(i);
        end
        
        idx = find(ptsMM(1,:)==-1);
        ptsPix(:,idx)=[];
        ptsMM(:,idx)=[];
        %         keyboard
        disp=nan(1,size(ptsMM,2));
        ptsPix=round(ptsPix);
        for i=1:size(ptsMM,2)
            delta=2;
            while isnan(disp(i))
            if ptsMM(1,i)==0 && ptsMM(2,i)==0
                neigh{i} = [ptsPix(2,i):ptsPix(2,i)+delta; ptsPix(1,i):ptsPix(1,i)+delta];
            elseif ptsMM(1,i)~=0 && ptsMM(2,i)==0
                neigh{i} = [ptsPix(2,i):ptsPix(2,i)+delta; ptsPix(1,i)-delta:ptsPix(1,i)];
            elseif ptsMM(1,i)~=0 && ptsMM(2,i)~=0
                neigh{i} = [ptsPix(2,i)-delta:ptsPix(2,i); ptsPix(1,i)-delta:ptsPix(1,i)];
            else
                neigh{i} = [ptsPix(2,i)-delta:ptsPix(2,i); ptsPix(1,i):ptsPix(1,i)+delta];
            end
            part{i} = i1(round(neigh{i}(1,:)),round(neigh{i}(2,:)));
            aux = reshape(part{i}, 1, (delta+1)^2);
%             keyboard
            idx = find(~isnan(aux) & aux<=1024);
            dd = i1(ptsPix(2,i),ptsPix(1,i));
%             if ~isnan(dd) && dd <= 1024
%                 disp(i)=dd;
%             else
            disp(i) = mode(aux(idx));
%             end
            delta=delta+5;
            end
            %             disp(i) = i1(ptsPix(2,i), ptsPix(1,i));
        end
       
%         disp
%         ptsPix
%          keyboard
        PlaneCornersInfo{imidx(N)}.disp=disp;
        PlaneCornersInfo{imidx(N)}.ptsMM=ptsMM;
        PlaneCornersInfo{imidx(N)}.ptsPix=ptsPix;
        clear disp ptsMM ptsPix
    else
        PlaneCornersInfo{imidx(N)}=[];
    end
    %     keyboard
    close(10);
    [ptsX,ptsY] = meshgrid(1:size(i1,2),1:size(i1,1));
%     X=X+[offs;-offs;-offs; offs];
%     Y=Y+[offs;offs; -offs; -offs];
    IN = inpolygon(ptsX,ptsY,X,Y);
%     figure, imshow(IN);
    IN = imerode(IN, true(offs));
%     figure, imshow(IN);
%     keyboard
    depth_plane_mask{N} = IN;
    
    %     i
    %     keyboard
end
save(['CPfiles/CP_' num2str(Nimsvar) 'C.mat'],'depth_plane_mask','dfiles');
save(['PlaneCornersInfo' num2str(Nimsvar) '.mat'],'PlaneCornersInfo');