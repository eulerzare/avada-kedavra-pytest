struct Empty {}

struct Response {
  1: i32 status,
  2: string message
}

enum AccountType {
    NULL = 0,
    INTERNAL = 1,
    EXTERNAL = 2
}

enum Genre {
    NULL = 0,
    MAIN = 1,
    CROSS_MARGIN = 2,
    ISOLATED_MARGIN = 3,
    TRADING_BOT = 4,
    STAKING = 5,
    PORTFOLIO = 6,
    OTHER = 7
}

enum Currency {
    NULL = 0,
    IRT = 1,
    USDT = 2,
    BTC = 3,
    ETH = 4
}