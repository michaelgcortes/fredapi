# How to work with APIs from Python and R

# Problem set up: 
# You need data, and there exists some API that you can get it from. 
# You want to do it in Python and/or R.
# How to do it? 


# Packages to load (make sure to install them before hand using function 'install.packages()')
packages.to.load <- c('httr', 'dplyr', 'lubridate')

lapply(packages.to.load, require, character.only=TRUE)


# Function to wrap around FRED API to provide R interface
fredr <- function(series.id, start.date, units){

    # Requested key from FRED API website. You must make an account. 
    api.key <- 'cbf1882aeb32943dc6a1ad50ceb1502a'

    # This is the generic URL scheme with values plugged in
    url <- paste0(
                 'https://api.stlouisfed.org/fred/series/observations?series_id=', 
                 series.id,
                 '&api_key=', 
                 api.key, 
                 '&file_type=json&observation_start=',
                 start.date,
                 '&units=', 
                 units
                )


    # Make the request using the 'requests' package using the GET method
    response <- httr::GET(url)

    # If successful, extract the results
    if(httr::status_code(response) == 200){

        # Extract the content from the response
        data.raw <- httr::content(response)
        obs.data <- data.raw$observations

        # Parse the raw data into a dataframe
        dates <- c()
        values <- c()
        for(i in 1:length(obs.data)){
            dates <- c(dates, obs.data[[i]]$date)
            values <- c(values, obs.data[[i]]$value)
        }

        data <- data.frame(cbind(dates, values)) %>% mutate(values = as.numeric(values))

        colnames(data)[2] <- series.id

        return(data)
    } else {
        print('The request failed.')
        return(NULL)
    }


}


# Run R function to get data from FRED API 
df <- fredr(series.id = 'GDP', start.date='2010-01-01', units='lin')

# Preview the data
head(df)