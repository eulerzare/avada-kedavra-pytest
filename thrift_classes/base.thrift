struct Empty {}

struct StatusResponse {
  1: i32 status,
  2: string message
}

enum AccountType {
    INTERNAL = 1,
    EXTERNAL = 2
}

enum Genre {
    MAIN = 1,
    CROSS_MARGIN = 2,
    ISOLATED_MARGIN = 3,
    TRADING_BOT = 4,
    STAKING = 5,
    PORTFOLIO = 6,
    OTHER = 7
}
