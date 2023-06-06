library(tidyverse)
library(manifestoR)
mp_setapikey("manifesto_apikey.txt")

mp_maindataset() %>%
  filter(countryname == "United Kingdom",
         edate >= as.Date("1964-01-01"),
         partyname %in% c("Conservative Party","Labour Party","Liberal Democrats","Liberal Party")) %>%
  mutate(manifesto = paste(party,date,sep="_")) %>%
  select(edate,partyname,manifesto) -> manifesto_list

manifestos <- mp_corpus(countryname == "United Kingdom" & edate >= as.Date("1964-01-01") & partyname %in% c("Conservative Party","Labour Party","Liberal Democrats","Liberal Party","Social Democratic Party"))

combine_text <- function(text) {
  paste(text,collapse = " ")
}

texts <- lapply(manifestos,combine_text)

texts %>%
  enframe(name = "manifesto", value = "text") %>%
  unnest(text) %>%
  inner_join(manifesto_list) %>%
  write_csv("data/manifestos.csv")