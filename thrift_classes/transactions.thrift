include "base.thrift"

service TransactionService {
  base.Response submitTransaction(1:TransactionBulk transactionBulk)
}

struct Transaction {
  1: required i64 entityId,
  2: required base.Genre genre,
  3: required base.AccountType accountType,
  4: required i32 pairId,
  5: required base.Currency currency,
  6: required string amount,
  7: required string freezeAmount,
  8: string minAmount,
  9: string subsidiaryAccount,
  10: string description
}

struct TransactionBulk {
  1: required string uniqueId,
  2: i64 timestamp,
  3: i64 objectId;
  4: string eventType;
  5: list<Transaction> transactions
}
