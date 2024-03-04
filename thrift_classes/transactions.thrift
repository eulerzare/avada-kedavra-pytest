include "base.thrift"

service TransactionService {
  base.StatusResponse submitTransaction(1:TransactionBulk transactionBulk)
}

struct Transaction {
  1: required string traderId,
  2: required base.Genre genre,
  3: required base.AccountType accountType,
  4: required i32 pairId,
  5: required string currencySymbol,
  6: required string amount,
  7: required string freezeAmount,
  8: required string minAmount,
}

struct TransactionBulk {
  1: required string uniqueId,
  2: i64 timestamp,
  3: list<Transaction> transactions
}
