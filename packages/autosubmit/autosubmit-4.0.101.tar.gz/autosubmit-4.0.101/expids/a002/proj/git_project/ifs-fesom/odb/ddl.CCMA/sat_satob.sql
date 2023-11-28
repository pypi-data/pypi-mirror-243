UPDATED;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sat_satob AS
  SELECT seqno READONLY,                   // r/o; MUST BECOME FIRST
         satellite_identifier@sat READONLY,               // r/o
         comp_method READONLY,             // r/o
         tb@satob READONLY,                // r/o
         height_assignment_method READONLY,  // r/o
         t@satob,                 // possibly updated
         zenith,            // possibly updated
         shear@satob,             // possibly updated
         t200@satob,              // possibly updated
         t500@satob,              // possibly updated
         top_mean_t@satob,        // possibly updated
         top_wv@satob,            // possibly updated
         dt_by_dp@satob,          // possibly updated
         p_best@satob,            // possibly updated
         u_best@satob,            // possibly updated
         v_best@satob,            // possibly updated
         p_old@satob,             // possibly updated
         u_old@satob,             // possibly updated
         v_old@satob,             // possibly updated
         tracking_error_u,        // possibly updated
         tracking_error_v,        // possibly updated
         h_assignment_error_u,    // possibly updated
         h_assignment_error_v,    // possibly updated
         error_in_h_assignment,   // possibly updated
         ct_p@satob,              // possibly updated
         cb_p@satob,              // possibly updated
         umod_old@satob,          // possibly updated
         vmod_old@satob,          // possibly updated
    FROM timeslot_index, index, hdr, sat, satob
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset
     AND obstype = $satob 
 ORDERBY seqno
;
