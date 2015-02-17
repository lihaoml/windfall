
module Main where
import Finance.Quote.Yahoo
import Data.Time.Calendar
import Data.Map 

-- quoteSymbolList = ["AAPL"] :: [QuoteSymbol]
quoteSymbolList = ["BN4.SI"] :: [QuoteSymbol]
quoteFieldsList = ["s","l1","c"] :: [QuoteField]

main = do
  q <- getQuote quoteSymbolList quoteFieldsList
  case q of
    Nothing -> error "no map"
    Just m -> case (Data.Map.lookup ("BN4.SI","l1") m) of
                   Nothing -> print "no match"
                   Just a -> print a
  let startDate = Data.Time.Calendar.fromGregorian 2013 07 01
  let endDate = Data.Time.Calendar.fromGregorian 2015 02 15
  h <- getHistoricalQuote (head quoteSymbolList) startDate endDate Daily
  case h of 
    Nothing -> error "no historical"
    Just l -> sequence $ Prelude.map print l
  return ()