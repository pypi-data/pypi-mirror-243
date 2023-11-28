UPDATED;
CREATE VIEW psbiashdr AS
SELECT seqno,
//       1
  obstype, code_type, instrument_type, date, time, source, statid,
//  2          3          4              5     6      7       8   
  lat, lon, stalt, modoro, anemoht, baroht, numlev, subtype, bufrtype, station_type,
//  9   10    11     12       13      14      15      16        17         18
// bias_correction_on, bc_info,
   reserved_0, bc_info,
// 19                    20
  variable_no, vertical_coordin_type, order_no, vertical_coordin, observed_value,
//     21             22                 23            24               25   
  biascorr_ind, biascorr, pressure_code, departure, previous_departure,
//      26        27            28          29              30
//
  kl_weight, kl_current_bias_estimate, kl_previous_bias_estimate, kl_current_variance, kl_previous_variance,
//      31               32                        33                     34                     35
  kl_current_obserr, kl_previous_obserr, kl_c_parameter, kl_long_term_bias, reserved_1,
//      36                    37                38          39                 40
  oi_weight, oi_current_bias_estimate, oi_previous_bias_estimate, oi_current_variance, oi_previous_variance,
//      41            42                       43                       44                    45
  oi_current_obserr, oi_previous_obserr, oi_q_varance, oi_bias_err_estimate, oi_long_term_bias,
//      46                  47                48                49              50
  long_term_sample_size, long_term_mean_departure, long_term_bias, long_term_std, long_term_rms,
//      51                        52                  53               54            55 
  biascorr_applied,
//      56
  report_status, report_event_1, report_event_2, report_rdb_flag, report_blacklist,
//      57            58             59                60               61
  ps_status, ps_event_1, ps_event_2, ps_blacklist, ps_flag, ps_rdb_flag,
//      62      63           64           65         66         67   
  body.offset, body.len
//   68          69
FROM hdr
//WHERE
;
