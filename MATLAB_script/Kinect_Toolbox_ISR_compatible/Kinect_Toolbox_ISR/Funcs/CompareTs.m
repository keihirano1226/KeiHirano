function [norm_t, theta_R] = CompareTs(Tref, Test)
% [norm_t, theta_R] = genCompareTs(Tref, Test)
% 
% Compare two reference frames.
% 
% Given two reference frames represented by 4-by-4 transformation matrices
% [Tref] and [Test], compute the absolute translation [norm_t] between
% them, as well as the rotation angle [theta_R] between them. The rotation
% angle is taken from the axis-angle representation of the rotation between
% the two frames.

	t_ref = Tref(1:3, 4);
	t_est = Test(1:3, 4);
	norm_t = norm(t_ref - t_est);
	
	Rref = Tref(1:3, 1:3);
	Rest = Test(1:3, 1:3);
	theta_R = norm(rodrigues(transpose(Rest)*Rref))*180/pi;
% 	theta_R = vrrotmat2vec(transpose(Rest)*Rref)*180/pi;
% 	theta_R = theta(4)
end