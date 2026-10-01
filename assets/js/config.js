/* 7Blockchain.com — single place for everything you may want to change.
   Edit values here; no other file needs touching. */
window.SITE = {
  name: "7Blockchain.com",
  url: "https://7blockchain.com",
  contactPageUrl: "https://web.works/contact",

  /* Contact pipeline. The destination address is assembled at runtime and is never
     printed in page text. Leave formEndpoint empty to use the visitor's mail client
     (mailto:). Optional upgrade: set formEndpoint to a FormSubmit/Formspree endpoint
     (e.g. "https://formsubmit.co/ajax/<your-hash>") to receive form posts without
     the visitor's mail client. */
  contactKey: "bW9jLmxpYW1nQDFhc2tyb3diZXc=",
  formEndpoint: "",

  /* Google AdSense: set your publisher ID (ca-pub-XXXXXXXXXXXXXXXX) to activate all slots.
     Also replace the line in /ads.txt. Slots stay as neutral placeholders until set. */
  adsenseClient: "",
  adSlots: { leader: "", rect: "", sky: "", anchor: "" },

  /* Analytics (optional): Google Analytics 4 measurement ID, e.g. "G-XXXXXXXXXX" */
  ga4: "",

  /* YouTube: channel handle for the subscribe buttons */
  youtubeChannel: "https://www.youtube.com/@7blockchain",

  /* Social links shown in footer (leave empty to hide) */
  social: { x: "https://x.com/7blockchain", youtube: "https://www.youtube.com/@7blockchain", telegram: "", linkedin: "", reddit: "", github: "https://github.com/webworksa1/7Blockchain-com" },

  /* Donations / support. Replace placeholders with your own addresses & links. */
  donate: {
    btc: "bc1q-REPLACE-WITH-YOUR-BITCOIN-ADDRESS",
    eth: "0xREPLACE-WITH-YOUR-ETHEREUM-ADDRESS",
    sol: "REPLACE-WITH-YOUR-SOLANA-ADDRESS",
    usdc: "0xREPLACE-WITH-YOUR-USDC-ERC20-ADDRESS",
    buymeacoffee: "https://www.buymeacoffee.com/7blockchain",
    paypal: "https://www.paypal.com/paypalme/7blockchain",
    githubSponsors: "https://github.com/sponsors/webworksa1",
    goalLabel: "Q4 2026 operations, promotion & contest prizes",
    goalTarget: 7000,
    goalRaised: 0
  },

  /* Affiliate / outbound link map. /go/?to=<key> redirects here. Add your tracked links. */
  go: {
    binance: "https://www.binance.com/",
    coinbase: "https://www.coinbase.com/",
    kraken: "https://www.kraken.com/",
    bybit: "https://www.bybit.com/",
    okx: "https://www.okx.com/",
    bitget: "https://www.bitget.com/",
    cryptocom: "https://crypto.com/",
    ledger: "https://www.ledger.com/",
    trezor: "https://trezor.io/",
    tangem: "https://tangem.com/",
    metamask: "https://metamask.io/",
    phantom: "https://phantom.app/",
    trustwallet: "https://trustwallet.com/",
    rabby: "https://rabby.io/",
    koinly: "https://koinly.io/",
    coinledger: "https://coinledger.io/",
    cointracker: "https://www.cointracker.io/",
    zenledger: "https://www.zenledger.io/",
    tokentax: "https://tokentax.co/",
    cryptotaxcalculator: "https://cryptotaxcalculator.io/",
    accointing: "https://www.blockpit.io/",
    aave: "https://aave.com/", uniswap: "https://uniswap.org/", lido: "https://lido.fi/",
    makerdao: "https://sky.money/", curve: "https://curve.fi/", jupiter: "https://jup.ag/", pendle: "https://www.pendle.finance/",
    arbitrum: "https://arbitrum.io/", optimism: "https://www.optimism.io/", base: "https://www.base.org/",
    polygon: "https://polygon.technology/", zksync: "https://zksync.io/", starknet: "https://www.starknet.io/", scroll: "https://scroll.io/",
    bitcoin: "https://bitcoin.org/", ethereum: "https://ethereum.org/", solana: "https://solana.com/",
    bnbchain: "https://www.bnbchain.org/", avalanche: "https://www.avax.network/", cardano: "https://cardano.org/", ton: "https://ton.org/",
    nexo: "https://nexo.com/", wirex: "https://wirex.com/", gnosispay: "https://gnosispay.com/", bybitcard: "https://www.bybit.com/en/cards/", coinbasecard: "https://www.coinbase.com/card", cryptocomcard: "https://crypto.com/cards"
  },

  /* Current contest (shown on /contests/). Set active:false to hide. */
  contest: {
    active: true,
    title: "7Blockchain Launch Quiz Challenge",
    prize: "$700 in prizes: $350 / $200 / $150 (paid in USDC or gift cards)",
    deadline: "2026-12-07T23:59:00Z",
    sponsor: "Sponsor this contest — see /advertise/",
    rules: "Score 7/7 on the Crypto Basics Quiz, submit the entry form with your score screenshot, one entry per person, winners drawn at random among perfect scores and announced in the 7-in-7 Digest."
  }
};
