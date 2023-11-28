//
// Created by J. Munoz Sabater - 21/02/2012
//

UPDATED;


CREATE VIEW update_modstep AS
  SELECT numtsl READONLY,
         model_timestep,
FROM   desc, timeslot_index
;
