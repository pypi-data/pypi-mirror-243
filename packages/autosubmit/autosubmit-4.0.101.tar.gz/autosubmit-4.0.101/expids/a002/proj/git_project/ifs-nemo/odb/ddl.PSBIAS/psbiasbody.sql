UPDATED;
CREATE VIEW psbiasbody AS
SELECT seqno, 
//       1
       history_date, history_time, history_departure,
//       2                 3                      4
       history_kl_bias,
//       5
       history_kl_weight, history_kl_variance, history_kl_obserr, history_kl_c_parameter,
//       6                 7                      8                   9
       history_oi_bias,
//      10
       history_oi_weight, history_oi_variance, history_oi_obserr, history_oi_q_varance, history_oi_err_estimate,
//      11                12                     13                  14                      15
       history_bc_info,
//      16
       history_report_status, history_report_event_1, history_report_event_2, history_report_rdb_flag,
//      17                      18                         19                      20
       history_report_blacklist,
//      21
       history_ps_status, history_ps_event_1, history_ps_event_2, history_ps_blacklist,
//      22                      23                         24                      25
       history_ps_flag, history_ps_rdb_flag,
//      26                      27
       history_biascorr_ind, history_biascorr, history_biascorr_applied
//      28                      29               30
FROM  hdr, body
//WHERE
;

