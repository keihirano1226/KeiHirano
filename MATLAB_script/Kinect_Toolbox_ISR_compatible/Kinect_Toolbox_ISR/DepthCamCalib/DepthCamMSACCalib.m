function [best_T, best_inliers, best_sample, min_cost] = DepthCamMSACCalib(PIcam,PIdep,threshold)

N_PLANES = size(PIcam,2);

plane_set = nchoosek(1:N_PLANES,3);

min_cost = inf;
for i = 1:size(plane_set,1)
    T_set = DepthCam3PlaneCalibNewRegist2(PIcam(:,plane_set(i,:)), PIdep(:,plane_set(i,:))); %CHANGED 

    error = nan(1,N_PLANES);
    for m = 1:size(T_set,3)
        error(m,:) = DepthCamCalibError(T_set(:,:,m), PIcam, PIdep);
        inliers    = union(find(error(m,:) < threshold),plane_set(i,:));
        cost       = sum(error(m,inliers).^2) + threshold^2*(size(error,2)-length(inliers));
%         cost = cost / length(inliers);
        if cost < min_cost
            min_cost     = cost;
            best_inliers = inliers;
            best_T       = T_set(:,:,m);
            best_sample  = plane_set(i,:);
        end
    end
    A(:,:,i) = inv(T_set);
end

% save Depth_RegAll.mat A