library(tidyverse)
library(manifestoR)
mp_setapikey("manifesto_apikey.txt")

# Get all the manifestos from the UK from 2019 for selected parties (Labour, Conservatives, and Lib Dems and predecessors)
uk_corpus <- mp_corpus(countryname == "United Kingdom" & edate >= as.Date("2019-01-01") & partyname %in% c("Labour Party","Liberal Democrats","Conservative Party"))
manifestos <- lapply(uk_corpus,content)

# Get the ids for all the selected manifestos
mp_maindataset() %>% 
  filter(countryname == "United Kingdom",
         edate >= as.Date("2019-01-01"),
         partyname %in% c("Labour Party",
                          "Liberal Democrats",
                          "Conservative Party")) %>%
  mutate(manifesto_id = paste(party,date,sep="_")) %>%
  pull(manifesto_id) -> manifesto_ids

