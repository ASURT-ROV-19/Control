RovModel = idnlgrey('mymodel',[1;1;2],[1;1;15],[]);
% Define an grey model 
%( my model is the CMEX file we wrote and compiled) 
%( Code is in Desktop/Hana)
%( The Order 1 Output / 1 Input /2 State Variables)
%( The 5,5,5 is the Parameters "we want to estimate" initial values)
%( []=> intital states for the ROV)
y = pressure;
%random data for output
u= pwms;
%u=randn(100,1);
%U
%data for input => Q here was defined as a shared CSV file between the matlab 
%and the python script

data = iddata(y, u, 0.1, 'Name', 'Rov');
%The data we will feed to the testing

Estimated_Model = nlgreyest(data,RovModel);
%This line of code will estimate the grey model for M4

plot(data);

