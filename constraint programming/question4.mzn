% Guillaume Thibault : 1948612
% Jacob Brisson : 1954091

include "globals.mzn";

int: n_nurse; % Number of nurses
int: n_week; % Number of weeks in our horizon
int: n_day; % Number of days in our horizon (7 * n_week). Monday is the first day of the week
int: n_work_period; % Number of work period. It equals 4 (MATIN, SOIREE, NUIT, REPOS)

% Indexing the work periods
int: MATIN = 1;
int: SOIREE = 2;
int: NUIT = 3;
int: REPOS = 4;

int: dur_work_period; % Duration of the work periods (6h)

array[1..n_day,1..n_work_period] of int: demande_min; % Number of nurses required for each day and each work period (= 0 for REPOS)
array[1..n_nurse,1..n_day,1..n_work_period] of int: preference; % Work preference for each nurse

% Decision variables
array[1..n_nurse,1..n_day,1..n_work_period] of var 0..1: x; % work period [MATIN, SOIREE, NUIT, REPOS]
var int: sum_preference;

% ~~~ CONTRAINTES ~~~~~~~~~~

% Infirmière travaillant de nuit est au repos à la période suivant
constraint
  forall(nurse in 1..n_nurse, day in 1..(n_day-1)) (
      if x[nurse, day, NUIT] == 1 then x[nurse, day + 1, REPOS] == 1 endif
  )
;

% Satisfere demande min
constraint 
  forall(day in 1..n_day, period in 1..n_work_period) (
     sum([ x[nurse, day, period] | nurse in 1..n_nurse ]) >= demande_min[day, period]
  )
;

% Infirmieres ont un chiffre par jours
constraint
  forall(nurse in 1..n_nurse, day in 1..n_day) (
      sum([ x[nurse, day, p] | p in 1..n_work_period ]) == 1
  )
;

% Max 3 jours de suite
constraint
  forall(nurse in 1..n_nurse, day in 1..(n_day-3)) (
      if (x[nurse, day, REPOS] != 1 /\ x[nurse, day+1, REPOS] != 1 /\ x[nurse, day + 2, REPOS] != 1) then x[nurse, day + 3, REPOS] == 1 endif
  )
;

% Max 36h semaine
constraint
  forall(nurse in 1..n_nurse, week in 1..n_week) (
     sum([ x[nurse, day+(7*(week-1)), p] | day in 1..7, p in 1..3]) <= 36/dur_work_period 
  )
;

% Min travailler 4 jours par semaine
constraint
  forall(nurse in 1..n_nurse, week in 1..n_week) (
     sum([ x[nurse, day+(7*(week-1)), p] | day in 1..7, p in 1..3]) >= 4
  )
;

% Aucun jour de travaille isole: INTERDIT -> repos - travail - repos
constraint
  forall(nurse in 1..n_nurse, day in 1..(n_day-2)) (
      if (x[nurse, day, REPOS] == 1 /\ x[nurse, day+1, REPOS] == 0) then x[nurse, day + 2, REPOS] != 1 endif
  )
;

% On veut maximiser la somme des préférences des infirmières
constraint sum_preference = sum(i in 1..n_nurse, j in 1..n_day, k in 1..n_work_period where x[i,j,k]==1)(preference[i,j,k]);

solve maximize sum_preference;


output
[
  "total: " ++ show(sum_preference) ++ "\n" ++
  "solution:\n\t    "
]
++
["Day \(j)\t" | j in 1..n_day]
++ 
[ 
  if j = 1 then "\n NURSE \(i): " else "\t" endif ++
    if fix(x[i,j,4]) == 1 then "--" elseif fix(x[i,j,3]) == 1  then "NUIT" elseif fix(x[i,j,2]) == 1  then "SOIREE" elseif fix(x[i,j,1]) == 1 then "MATIN" else "NONE" endif
  | i in 1..n_nurse, j in 1..n_day
];

