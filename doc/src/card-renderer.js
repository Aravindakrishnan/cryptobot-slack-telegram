const commands = [
    {
        id : 1,
        name : "/getprice",
        option : "[coin_name] or [coin_symbol]",
        desc : "returns the current price of the coin default : USD"
    },
    {
        id : 2,
        name : "/getprice",
        option : "[coin_name] or [coin_symbol] [fiat_name]",
        desc : "returns the current price of the coin in fiat"
    },
    {
        id : 3,
        name : "/getdetail",
        option : "[coin_name] or [coin_symbol]",
        desc : "returns the complete detail about the current cryptocurrency"
    },
    {
        id : 4,
        name : "/getdetail",
        option : "[coin_name] or [coin_symbol] [fiat_name]",
        desc : "returns the complete detail about the current cryptocurrency with specific fiat price"
    },
    {
        id : 5,
        name : "/showcandle",
        option : "[coin_name or coin_symbol]",
        desc : "the candle graph snapshot of the particular coin <br> default : 1d"
    },
    {
        id : 6,
        name : "/showcandle",
        option : "[coin_name or coin_symbol] [1m,3m,5m,15m,30m,1h,2h,\n4h,6h,8h,12h,1d,3d,1w,1M]",
        desc : " return the candle graph snapshot of the particular coin's specific timeframe"
    }


]

const template = commands.map(command=> {

    return (
        `
        <div id=usage_card${command.id} class="usage__content">
        <span class="usage__command">${command.name}</span>
        <span class="usage__options">${command.option}</span>
        <p class="usage__desc">${command.desc}</p>
        </div>
        `
    )

})

document.querySelector(".usage-container").innerHTML = template.join("");

// isActive

function isActive(status){
    const template = `<span class="server_status">status : ${ status ? "active" : "inactive" }</span>`
    return {isactive : status , template}
}

function renderSlackStatus(status){
    const slack_element = document.querySelector(".slack__status")
    slack_element.innerHTML = status.template
    if(status.isactive){
        slack_element.classList.add("active")
        return
    }
    slack_element.classList.add("inactive")
}

function renderTelegramStatus(status){
    const telegram_element = document.querySelector(".telegram__status");
    telegram_element.innerHTML = status.template
    if(status.isactive){
        telegram_element.classList.add("active")
        return
    }
    telegram_element.classList.add("inactive")
}

const isActiveTelegram = isActive(false)
const isActiveSlack = isActive(true)

renderSlackStatus(isActiveSlack)
renderTelegramStatus(isActiveTelegram)

