function varargout = CalibGUI(varargin)
% CALIBGUI MATLAB code for CalibGUI.fig
%      CALIBGUI, by itself, creates a new CALIBGUI or raises the existing
%      singleton*.
%
%      H = CALIBGUI returns the handle to a new CALIBGUI or the handle to
%      the existing singleton*.
%
%      CALIBGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in CALIBGUI.M with the given input arguments.
%
%      CALIBGUI('Property','Value',...) creates a new CALIBGUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before CalibGUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to CalibGUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help CalibGUI

% Last Modified by GUIDE v2.5 20-Sep-2013 16:03:47

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @CalibGUI_OpeningFcn, ...
    'gui_OutputFcn',  @CalibGUI_OutputFcn, ...
    'gui_LayoutFcn',  [] , ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before CalibGUI is made visible.
function CalibGUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to CalibGUI (see VARARGIN)
rmpath('bouguet/toolbox_calib');
addpath('Kinect_Toolbox/toolbox');
addpath('Funcs');
addpath('DepthCamCalib');
addpath('EstimateDistModel');
% Choose default command line output for CalibGUI
handles.output = hObject;
% handles.Nfix = 0;
% Update handles structure
guidata(hObject, handles);

% UIWAIT makes CalibGUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = CalibGUI_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function Nimages_Callback(hObject, eventdata, handles)
% hObject    handle to Nimages (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Nimages as text
%        Nfix=str2double(get(hObject,'String')); %returns contents of Nimages as a double
handles.Nfix = str2double(get(hObject,'String'));
guidata(hObject, handles);


% --- Executes during object creation, after setting all properties.
function Nimages_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Nimages (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function image_numbers_Callback(hObject, eventdata, handles)
% hObject    handle to image_numbers (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of image_numbers as text
%        str2double(get(hObject,'String')) returns contents of image_numbers as a double

handles.imNums = strread(get(hObject,'String'));
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function image_numbers_CreateFcn(hObject, eventdata, handles)
% hObject    handle to image_numbers (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in RGBcorners.
function RGBcorners_Callback(hObject, eventdata, handles)
% hObject    handle to RGBcorners (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
imNums = handles.imNums;
Nimsvar=handles.Nfix;
create_CalibBou_GUI;
handles.fileBou = ['BouFiles/BouCalibRes_' num2str(Nimsvar) 'C.mat'];
guidata(hObject, handles);

% --- Executes on button press in depthcorners.
function depthcorners_Callback(hObject, eventdata, handles)
% hObject    handle to depthcorners (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
imNums = handles.imNums;
Nimsvar=handles.Nfix;
create_CPfile_GUI_v2;
handles.fileCP = ['CPfiles/CP_' num2str(N) 'C.mat'];
handles.filePlane = ['PlaneCornersInfo' num2str(N) '.mat'];
guidata(hObject, handles);

% --- Executes on button press in calib.
function calib_Callback(hObject, eventdata, handles)
% hObject    handle to calib (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

Nimsvar=handles.Nfix;
loadF=handles.fileBou;
fileCP=handles.fileCP;
planeinfo=handles.filePlane;
MyTB_Calib;
handles.resCalib = save_file;
guidata(hObject, handles);


% --- Executes on button press in distCorrection.
function distCorrection_Callback(hObject, eventdata, handles)
% hObject    handle to distCorrection (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
res_file = handles.resCalib;
fileBou=handles.fileBou;
fileCP=handles.fileCP;
Nimsvar=handles.Nfix;

EstDistortion;
handles.distCorr = ['MyTBCalibDistEst' num2str(Nimsvar) '.mat'];
guidata(hObject, handles);



% --- Executes on button press in ReprojErrors.
function ReprojErrors_Callback(hObject, eventdata, handles)
% hObject    handle to ReprojErrors (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
if ishandle(1)
    close(1)
end

if ishandle(2)
    close(2)
end
if ishandle(3)
    close(3)
end
Nimsvar=handles.Nfix;
res_file = handles.resCalib;
dist_file=handles.distCorr;
valIm=handles.valIm; %number of validation image
ComputeRMSerrorpix;


% --- Executes on button press in loadexs.
function loadexs_Callback(hObject, eventdata, handles)
% hObject    handle to loadexs (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
if ishandle(12)
    close(12)
end
Nimsvar=handles.Nfix;
handles.fileCP = ['CPfiles/CP_' num2str(Nimsvar) '.mat'];
handles.fileBou = ['BouFiles/BouCalibRes_' num2str(Nimsvar) '.mat'];
handles.filePlane = 'PlaneCornersInfo.mat';
guidata(hObject, handles);



function valIm_Callback(hObject, eventdata, handles)
% hObject    handle to valIm (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of valIm as text
%        str2double(get(hObject,'String')) returns contents of valIm as a double
handles.valIm = str2double(get(hObject,'String'));
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function valIm_CreateFcn(hObject, eventdata, handles)
% hObject    handle to valIm (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in OverlayFunc.
function OverlayFunc_Callback(hObject, eventdata, handles)
% hObject    handle to OverlayFunc (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
Nimsvar=handles.Nfix;
calibFile = load(handles.resCalib);
distFile = load(handles.distCorr);
% load('data/full_set.mat');
calib.dc = calibFile.INd.dc;
calib.dR=calibFile.Tdep2camout(1:3,1:3);
calib.dt=calibFile.Tdep2camout(1:3,4)/1000;
calib.dK=[calibFile.INd.fc(1) 0 calibFile.INd.cc(1)
    0 calibFile.INd.fc(2) calibFile.INd.cc(2)
    0 0 1];
calib.dkc = [0 0 0 0 0];
calib.rK{1}=[calibFile.INc.fc(1) calibFile.INc.alpha*calibFile.INc.fc(1) calibFile.INc.cc(1)
    0 calibFile.INc.fc(2) calibFile.INc.cc(2)
    0 0 1];
calib.rkc{1} = calibFile.INc.kc;
% idx = find(abs(calib.rkc{1})>1);
% calib.rkc{1}(idx)=calib.rkc{1}(idx)/10;
% calib.rkc{1}
% calib.rkc{1}=[0 0 0 0 0];
figure(12)
ss=[ 1024 1280];
% ss = [480 640];
imN=handles.imOver;
imD = sprintf('data/%04d-d.pgm', imN-1);
imR = sprintf('data/%04d-c1.jpg', imN-1);

% calib=final_calib;
if handles.isDC
    calib.dc_beta=distFile.meanMat;
    calib.dc_alpha=[0 distFile.a1];
else
    calib.dc_beta=zeros(480,640);
    calib.dc_alpha=[0 0];
end
plot_depth_overlayM(calib, ss, imR, imD,1);


function imOver_Callback(hObject, eventdata, handles)
% hObject    handle to imOver (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of imOver as text
%        str2double(get(hObject,'String')) returns contents of imOver as a double
handles.imOver = str2double(get(hObject,'String'));
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function imOver_CreateFcn(hObject, eventdata, handles)
% hObject    handle to imOver (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in isDC.
function isDC_Callback(hObject, eventdata, handles)
% hObject    handle to isDC (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of isDC
handles.isDC=get(hObject,'Value');
guidata(hObject, handles);


% --- Executes on button press in exportMesh.
function exportMesh_Callback(hObject, eventdata, handles)
% hObject    handle to exportMesh (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
addpath('ply');
Nimsvar=handles.Nfix;
calibFile = (handles.resCalib);
distFile = (handles.distCorr);
imN=handles.imOver;
CreateMeshGUI;
