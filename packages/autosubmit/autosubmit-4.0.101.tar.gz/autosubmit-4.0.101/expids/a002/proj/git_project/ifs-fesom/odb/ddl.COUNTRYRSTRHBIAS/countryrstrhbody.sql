READONLY;
CREATE VIEW countryrstrhbody AS
SELECT seqno, press,
//        1     2
       T_B_m75_vs_all_mean, T_B_m75_75_vs_all_mean, T_B_75_225_vs_all_mean, T_B_225_vs_all_mean, T_B_all_mean,
//        3                          4                        5                       6                  7
       RH_B_m75_vs_all_mean, RH_B_m75_75_vs_all_mean, RH_B_75_225_vs_all_mean, RH_B_225_vs_all_mean, RH_B_all_mean,
//        8                          9                       10                      11                 12 
       T_B_m75_vs_night_mean, T_B_m75_75_vs_night_mean, T_B_75_225_vs_night_mean, T_B_225_vs_night_mean, T_B_night_mean,
//       13                         14                       15                      16                 17
       RH_B_m75_vs_night_mean, RH_B_m75_75_vs_night_mean, RH_B_75_225_vs_night_mean, RH_B_225_vs_night_mean, RH_B_night_mean,
//       18                         19                       20                      21                 22 
       T_B_m75_vs_day_mean, T_B_m75_75_vs_day_mean, T_B_75_225_vs_day_mean, T_B_225_vs_day_mean, T_B_day_mean,
//       23                         24                       25                      26                 27
       RH_B_m75_vs_day_mean, RH_B_m75_75_vs_day_mean, RH_B_75_225_vs_day_mean, RH_B_225_vs_day_mean, RH_B_day_mean
//       28                         29                       30                      31                 32 
FROM  hdr, body
//WHERE
//ORDERBY
;

