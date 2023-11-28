CREATE VIEW pertcma AS
    SELECT obsvalue,fg_depar,final_obs_error,hires@update[1],hires@update[3]
      FROM hdr,body,errstat,update[1],update[3]
;
