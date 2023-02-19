library(tidyverse)
library(manifestoR)
mp_setapikey("manifesto_apikey.txt")

# Get all the manifestos from the UK from 1964 to 2019 for selected parties (Labour, Conservatives, and Lib Dems and predecessors)
uk_corpus <- mp_corpus(countryname == "United Kingdom" & edate >= as.Date("1964-01-01") & partyname %in% c("Labour Party","Liberal Party","Social Democratic Party","Liberal Democrats","Conservative Party"))
manifestos <- lapply(uk_corpus,content)

# Get the ids for all the selected manifestos
mp_maindataset() %>% 
  filter(countryname == "United Kingdom",
         edate >= as.Date("1964-01-01"),
         partyname %in% c("Labour Party",
                          "Liberal Party",
                          "Social Democratic Party",
                          "Liberal Democrats",
                          "Conservative Party")) %>%
  mutate(manifesto_id = paste(party,date,sep="_")) %>%
  pull(manifesto_id) -> manifesto_ids

# Function that concatenates manifestos into single string by id
get_text_from_manifesto <- function(manifestos, manifesto_id) {
  text <- paste(manifestos[[manifesto_id]], collapse = '')
  
  return(text)
}

# Apply this function to all the manifestos, create tibble
manifesto_texts <- lapply(manifesto_ids,function(x) get_text_from_manifesto(manifestos=manifestos,manifesto_id=x))
manifesto_df <- tibble(id = manifesto_ids, text = manifesto_texts) %>% unnest(text)

# Write tibble to csv
manifesto_df %>%
  write_csv("data/uk_manifestos.csv")
