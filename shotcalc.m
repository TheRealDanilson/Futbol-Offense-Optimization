function p = shotcalc(xpos,ypos)
%calcuting shooting probabilty
%xpos is the x position of the player with the ball
%ypos is the y position of the player with the ball
z = (xpos^2)/150 +(ypos^2)/300;
if z >= 4.5 || (xpos^2)/ypos > 30
    p = 0;
elseif sqrt((xpos^2)+(ypos^2))<= 5
    p = 1;
else
    p = expcdf((4.5-z),3.33);
end
