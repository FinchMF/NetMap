CREATE TABLE WordSearch (

    tweet_time VARCHAR(30),
    tweet_id int,
    full_text VARCHAR(300),
    text_range VARCHAR(30),



)

-- word search will be a table that contains results for a text from the 
 -- word search function (or phrase) -- this will have a base set of columns
  -- and a set of columns that are added through out  altering the table
    -- there will also be a table of followers with unique IDs
        -- i want to be able to connect the unique IDs of the accounts to text and other accounts
    -- additionally, this table will need to be automated, the altered based on setup files when 
    -- program is ran