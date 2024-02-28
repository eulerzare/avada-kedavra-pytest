include "base.thrift"

service TraderService {
  AddTraderResponse addTrader(1:AddTrader addTrader)
  GetTradersAccountsResponse getTradersAccounts(1: RequestGetTraderAccount requestGetTraderAccount)
}

struct AddTrader {
  1: required string uniqueId,
}

struct AddTraderResponse {
  1: i32 status,
  2: string message,
  3: string uniqueId
}

struct RequestGetTraderAccount {
  1: required list<string> traderIds
}

struct TraderAccount {
  1: string traderId
  2: string currencySymbol
  3: base.Genre genre,
  4: base.AccountType accountType,
  5: string balance,
  6: string freezeBalance,
  7: string minBalance,
}

struct GetTradersAccountsResponse {
  1: i32 status,
  2: string message,
  3: list<TraderAccount> traderAccount
}