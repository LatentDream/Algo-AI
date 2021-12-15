% Guillaume Thibault : 1948612
% Jacob Brisson : 1954091

include "globals.mzn"; 

int: n; % num rows and columns

int: L = 1; % Lamp
int: P = 2; % Plant

% 1 for a lamp, 2 for a plant and 0 for nothing 
array[1..n,1..n] of 0..2: garden;

% number of plants by row/col
array[1..n] of int: rows;
array[1..n] of int: cols;

% decision variables
array[1..n,1..n] of var 0..P: x;

% Initialiser les positions ou il y a des lampes
constraint forall(i in 1..n,j in 1..n)(if garden[i,j] == L then x[i,j] = L else true endif);

% Le nombre de plantes sur une ligne doit être égal à celui décrit. De plus, pour chaque lampe, il faut qu'il y ait au moins une plante à côté.
constraint forall(k in 1..n)((exactly_int(rows[k],row(x,k),P)) /\ (forall(j in 1..n)(if garden[k,j]==L then count(v in [x[k,min(j+1,n)],x[k,max(j-1,1)],x[max(k-1,1),j],x[min(k+1,n),j]])(v=P) >= 1 else true endif)));

% Le nombre de plantes sur une colonne doit être égal à celui décrit.
constraint forall(k in 1..n)(exactly_int(cols[k],col(x,k),P));

% Pour chaque plante, il doit y avoir au moins 1 lampe à côté. De plus, il ne doit pas y avoir de plante qui lui touche.
constraint forall(i in 1..n,j in 1..n)(if x[i,j] == P then count(v in [x[i,min(j+1,n)],x[i,max(j-1,1)],x[max(i-1,1),j],x[min(i+1,n),j]])(v=L) >= 1 /\ count(v in [x[e,f] | e in max(i-1,1)..min(i+1,n),f in max(j-1,1)..min(j+1,n) where f!=j \/ e!=i])(v=P) == 0 else true endif);

solve satisfy;

output 
[
 if j = 1 then "\n" ++ show(rows[i]) ++ " " else " " endif ++
   if fix(x[i,j]) = L then "L" elseif fix(x[i,j]) = P then "P" else "_" endif
| i,j in 1..n
] ++ ["\n  "] ++ [show(cols[i]) ++ " " | i in 1..n];
