% Guillaume Thibault : 1948612
% Jacob Brisson : 1954091

include "globals.mzn"; 

int: n = 5;
% the given results
array[1..4] of int: res = [1,2,5,7];

% number of points for each player
array[1..n] of var 0..3*n: x;

% (i, j) is the result of player i against player j
array[1..n, 1..n] of var {0,1,3}: matches;

% Les scores totaux des joueurs 1 à 4 doivent correspondre à leur score final et ils ne peuvent pas avoir de points en jouant contre eux-mêmes
constraint forall(k in 1..n-1)(sum(row(matches,k))==res[k] /\ matches[k,k]=0);

% Le nombre de points de chaque joueur est égal à la somme de ses gains lors de ses matchs
constraint forall(k in 1..n)(x[k]=sum(row(matches,k)));

% Si un joueur à gagné contre un autre, l'autre à alors perdu sont match et vice-versa. Sinon, s'il y a eu match nul, alors les deux gagnent 1 point.
constraint forall(i in 1..n, j in 1..n where i!=j)(if matches[i,j] == 1 then matches[j,i] = 1 else true endif /\if matches[i,j]==3 then matches[j,i] == 0 else true endif /\if matches[i,j] == 0 then matches[j,i]=3 else true endif);

solve satisfy;

output 
[
  "Scores\n"
]
++
[
  show(x)
]
++	
[
  "\nMatches\n"
]
++
[ show(matches[i,j]) ++ 
         if j == n then "\n" else " " endif |
         i in 1..n, j in 1..n
]
;