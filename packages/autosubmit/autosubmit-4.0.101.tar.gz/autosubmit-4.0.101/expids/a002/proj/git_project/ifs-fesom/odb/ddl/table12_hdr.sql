READONLY;
CREATE VIEW table12_hdr AS
SELECT seqno,
//        1 
       active_line, active_inactive_seqno, country_group,
//        2                    3                4
       country_name_1, country_name_2, country_name_3, country_name_4, country_name_5, country_name_6, country_name_7, country_name_8
//          5                 6              7                8            9               10              11              12
FROM era_country_t_table12_hdr
;
