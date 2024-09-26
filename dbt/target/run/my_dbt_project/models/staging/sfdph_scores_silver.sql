
  
    

    create or replace table `powerful-rhino-436521-b5`.`data_prep`.`sfdph_scores_silver`
      
    
    

    OPTIONS()
    as (
      SELECT UPPER(business_name) as business_name
, address
, UPPER(purpose) as purpose
, PARSE_DATE('%B %d, %Y', inspection_date) as inspection_date
, UPPER(facility_rating_status) as facility_rating_status
FROM `external_data`.`sfdph_scores_bronze`
GROUP BY 1,2,3,4,5
    );
  