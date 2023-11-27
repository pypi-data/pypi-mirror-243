export const getBrowser = () => {
  const unknown = '-'

  // screen
  let screenSize = ''
  if (screen.width) {
    const width = (screen.width) ? screen.width : ''
    const height = (screen.height) ? screen.height : ''
    screenSize += '' + width + ' x ' + height
  }

  // browser
  const nVer = navigator.appVersion
  const nAgt = navigator.userAgent
  let browser = navigator.appName
  let version = '' + parseFloat(navigator.appVersion)
  let majorVersion = parseInt(navigator.appVersion, 10)
  let nameOffset, verOffset, ix

  // Opera
  if ((verOffset = nAgt.indexOf('Opera')) !== -1) {
    browser = 'Opera'
    version = nAgt.substring(verOffset + 6)
    if ((verOffset = nAgt.indexOf('Version')) !== -1) {
      version = nAgt.substring(verOffset + 8)
    }
  }
  // Opera Next
  if ((verOffset = nAgt.indexOf('OPR')) !== -1) {
    browser = 'Opera'
    version = nAgt.substring(verOffset + 4)
  } else if ((verOffset = nAgt.indexOf('Edge')) !== -1) { // Legacy Edge
    browser = 'Microsoft Legacy Edge'
    version = nAgt.substring(verOffset + 5)
  } else if ((verOffset = nAgt.indexOf('Edg')) !== -1) { // Edge (Chromium)
    browser = 'Microsoft Edge'
    version = nAgt.substring(verOffset + 4)
  } else if ((verOffset = nAgt.indexOf('MSIE')) !== -1) { // MSIE
    browser = 'Microsoft Internet Explorer'
    version = nAgt.substring(verOffset + 5)
  } else if ((verOffset = nAgt.indexOf('Chrome')) !== -1) { // Chrome
    browser = 'Chrome'
    version = nAgt.substring(verOffset + 7)
  } else if ((verOffset = nAgt.indexOf('Safari')) !== -1) { // Safari
    browser = 'Safari'
    version = nAgt.substring(verOffset + 7)
    if ((verOffset = nAgt.indexOf('Version')) !== -1) {
      version = nAgt.substring(verOffset + 8)
    }
  } else if ((verOffset = nAgt.indexOf('Firefox')) !== -1) { // Firefox
    browser = 'Firefox'
    version = nAgt.substring(verOffset + 8)
  } else if (nAgt.indexOf('Trident/') !== -1) { // MSIE 11+
    browser = 'Microsoft Internet Explorer'
    version = nAgt.substring(nAgt.indexOf('rv:') + 3)
  } else if ((nameOffset = nAgt.lastIndexOf(' ') + 1) <
             (verOffset = nAgt.lastIndexOf('/'))) { // Other browsers
    browser = nAgt.substring(nameOffset, verOffset)
    version = nAgt.substring(verOffset + 1)
    if (browser.toLowerCase() === browser.toUpperCase()) {
      browser = navigator.appName
    }
  }
  // trim the version string
  if ((ix = version.indexOf(';')) !== -1) version = version.substring(0, ix)
  if ((ix = version.indexOf(' ')) !== -1) version = version.substring(0, ix)
  if ((ix = version.indexOf(')')) !== -1) version = version.substring(0, ix)

  majorVersion = parseInt('' + version, 10)
  if (isNaN(majorVersion)) {
    version = '' + parseFloat(navigator.appVersion)
    majorVersion = parseInt(navigator.appVersion, 10)
  }

  // mobile version
  const mobile = /Mobile|mini|Fennec|Android|iP(ad|od|hone)/.test(nVer)

  // cookie
  let cookieEnabled = !!(navigator.cookieEnabled)

  if (typeof navigator.cookieEnabled === 'undefined' && !cookieEnabled) {
    document.cookie = 'testcookie'
    cookieEnabled = (document.cookie.indexOf('testcookie') !== -1)
  }

  // test

  // system
  let os = unknown
  const clientStrings = [
    { s: 'Windows 10', r: /(Windows 10.0|Windows NT 10.0)/ },
    { s: 'Windows 8.1', r: /(Windows 8.1|Windows NT 6.3)/ },
    { s: 'Windows 8', r: /(Windows 8|Windows NT 6.2)/ },
    { s: 'Windows 7', r: /(Windows 7|Windows NT 6.1)/ },
    { s: 'Windows Vista', r: /Windows NT 6.0/ },
    { s: 'Windows Server 2003', r: /Windows NT 5.2/ },
    { s: 'Windows XP', r: /(Windows NT 5.1|Windows XP)/ },
    { s: 'Windows 2000', r: /(Windows NT 5.0|Windows 2000)/ },
    { s: 'Windows ME', r: /(Win 9x 4.90|Windows ME)/ },
    { s: 'Windows 98', r: /(Windows 98|Win98)/ },
    { s: 'Windows 95', r: /(Windows 95|Win95|Windows_95)/ },
    { s: 'Windows NT 4.0', r: /(Windows NT 4.0|WinNT4.0|WinNT|Windows NT)/ },
    { s: 'Windows CE', r: /Windows CE/ },
    { s: 'Windows 3.11', r: /Win16/ },
    { s: 'Android', r: /Android/ },
    { s: 'Open BSD', r: /OpenBSD/ },
    { s: 'Sun OS', r: /SunOS/ },
    { s: 'Chrome OS', r: /CrOS/ },
    { s: 'Linux', r: /(Linux|X11(?!.*CrOS))/ },
    { s: 'iOS', r: /(iPhone|iPad|iPod)/ },
    { s: 'Mac OS X', r: /Mac OS X/ },
    { s: 'Mac OS', r: /(Mac OS|MacPPC|MacIntel|Mac_PowerPC|Macintosh)/ },
    { s: 'QNX', r: /QNX/ },
    { s: 'UNIX', r: /UNIX/ },
    { s: 'BeOS', r: /BeOS/ },
    { s: 'OS/2', r: /OS\/2/ },
    { s: 'Search Bot', r: /(nuhk|Googlebot|Yammybot|Openbot|Slurp|MSNBot|Ask Jeeves\/Teoma|ia_archiver)/ }
  ]
  for (const id in clientStrings) {
    const cs = clientStrings[id]
    if (cs.r.test(nAgt)) {
      os = cs.s
      break
    }
  }

  let osVersion = unknown

  if (/Windows/.test(os)) {
    osVersion = /Windows (.*)/.exec(os)[1]
    os = 'Windows'
  }

  switch (os) {
    case 'Mac OS':
    case 'Mac OS X':
    case 'Android':
      osVersion = /(?:Android|Mac OS|Mac OS X|MacPPC|MacIntel|Mac_PowerPC|Macintosh) ([._d]+)/.exec(nAgt)[1]
      break

      // TODO case 'iOS':
      // TODO   osVersion = /OS (\d+)_(\d+)_?(\d+)?/.exec(nVer)
      // TODO   osVersion = osVersion[1] + '.' + osVersion[2] + '.' + (osVersion[3] | 0)
      // TODO   break
  }

  // flash (you'll need to include swfobject)
  /* script src="//ajax.googleapis.com/ajax/libs/swfobject/2.2/swfobject.js" */
  // TODO var flashVersion = 'no check'
  // TODO if (typeof swfobject !== 'undefined') {
  // TODO   const fv = swfobject.getFlashPlayerVersion()
  // TODO   if (fv.major > 0) {
  // TODO     flashVersion = fv.major + '.' + fv.minor + ' r' + fv.release
  // TODO   } else {
  // TODO     flashVersion = unknown
  // TODO   }
  // TODO }

  return {
    screen: screenSize,
    browser,
    browserVersion: version,
    browserMajorVersion: majorVersion,
    mobile,
    os,
    osVersion,
    cookies: cookieEnabled
    // TODO flashVersion: flashVersion
  }
}

// TODO alert(
// TODO   'OS: ' + jscd.os + ' ' + jscd.osVersion + '\n' +
// TODO     'Browser: ' + jscd.browser + ' ' + jscd.browserMajorVersion +
// TODO       ' (' + jscd.browserVersion + ')\n' +
// TODO     'Mobile: ' + jscd.mobile + '\n' +
// TODO     'Flash: ' + jscd.flashVersion + '\n' +
// TODO     'Cookies: ' + jscd.cookies + '\n' +
// TODO     'Screen Size: ' + jscd.screen + '\n\n' +
// TODO     'Full User Agent: ' + navigator.userAgent
// TODO )

// const Cookies = require('js-cookie')
// TODO const { DateTime } = require('luxon')
// const { nb60encode, nb60decode } = require('NewMath')

// export const cookies = Cookies
// TODO export const dt = DateTime
// _.nb60encode = nb60encode
// _.nb60decode = nb60decode

export const _ = (selector) => {
  const results = typeof selector === 'string'
    ? document.querySelectorAll(selector)
    : [selector]
  // const results = Array.prototype.slice.call(nodes)
  const items = {}
  for (let i = 0; i < results.length; i++) {
    items[i] = results[i]
  }
  items._ = _
  items.el = items[0]
  items.n = results.length
  // items.splice = [].splice() // simulates an array FIXME
  // items.each = callback => { nodes.forEach(callback, ) }
  items.each = callback => {
    for (let i = 0; i < results.length; i++) {
      callback(results[i])
    }
  }
  // for (let i = 0; i < results.length; i++) {
  //   console.log(results[i])
  //   results[i].addEventListener('click', () => { console.log('er') })
  // }
  // items.click = callback => {
  //   for (let i = 0; i < results.length; i++) {
  //     console.log(this.results[i], this)
  //     this.results[i].addEventListener('click', () => { console.log('er') })
  //     // callback.bind(nodes[i])
  //     // callback(nodes[i])
  //   }
  // }
  items.append = html => {
    items.each(item => item.appendChild(createEl(html)))
  }
  items.move = (left, top) => {
    items.el.style.left = left
    items.el.style.top = top
  }
  items.click = callback => {
    items.each(item => {
      item.addEventListener('click', callback)
    })
  }
  return items
}

export const createEl = html => {
  const template = document.createElement('template')
  template.innerHTML = html.trim()
  return template.content.firstChild
}

export const createEls = html => {
  const template = document.createElement('template')
  template.innerHTML = html
  return template.content.childNodes
}

const loadScripts = []
const unloadScripts = []
const executeLoadScripts = () => {
  loadScripts.forEach(handler => handler())
  loadScripts.length = 0
}
const executeUnloadScripts = () => {
  unloadScripts.forEach(handler => handler())
  unloadScripts.length = 0
}
document.addEventListener('DOMContentLoaded', () => executeLoadScripts())
window.addEventListener('beforeunload', () => {
  executeUnloadScripts()
})
export const load = handler => loadScripts.push(handler)
export const unload = handler => unloadScripts.push(handler)

export const mouseup = handler => document.addEventListener('mouseup', handler)
export const popstate = handler => window.addEventListener('popstate', handler)
export const online = handler => window.addEventListener('online', handler)
export const offline = handler => window.addEventListener('offline', handler)
export const error = handler => window.addEventListener('error', handler)

export const upgradeTimestamps = () => {
  // TODO const pageLoad = DateTime.now()
  // TODO _('time').each(item => {
  // TODO   item.setAttribute('title', item.innerHTML)
  // TODO   item.innerHTML = DateTime.fromISO(item.attributes.datetime.value)
  // TODO     .toRelative({ base: pageLoad })
  // TODO })
}

// --------------------------------------------------------------------------

// interface Configuration {
//   q?: string
//   'media-endpoint'?: string
//   'syndicate-to'?: string
//   'visibility'?: string
// }

export class MicropubClient {
  // endpoint: string
  // token: string
  // headers: any
  // config: Configuration

  constructor (endpoint, token) {
    this.endpoint = endpoint
    this.token = token
    this.headers = {
      accept: 'application/json'
    }
    if (typeof token !== 'undefined') {
      this.headers.authorization = `Bearer ${token}`
    }

    this.getConfig = this.getConfig.bind(this)

    this.create = this.create.bind(this)
    this.read = this.read.bind(this)
    this.update = this.update.bind(this)
    this.delete = this.delete.bind(this)

    this.query = this.query.bind(this)
    this.upload = this.upload.bind(this)
  }

  getConfig () {
    return fetch(this.endpoint + '?q=config', {
      headers: this.headers
    }).then(response => {
      if (response.status === 200 || response.status === 201) {
        return response.json().then(data => {
          return data
        })
      }
    })
  }

  getCategories () {
    return fetch(this.endpoint + '?q=category', {
      headers: this.headers
    }).then(response => {
      if (response.status === 200 || response.status === 201) {
        return response.json().then(data => {
          return data
        })
      }
    })
  }

  // create (type: string, properties: object, visibility?: string) {
  create (type, properties, visibility) {
    const headers = this.headers
    headers['content-type'] = 'application/json'
    if (typeof visibility === 'undefined') {
      visibility = 'private'
    }
    // TODO properties.visibility = visibility
    return fetch(this.endpoint, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        type: [`h-${type}`],
        properties
      })
    }).then(response => {
      if (response.status === 200 || response.status === 201) {
        return response.headers.get('location') // permalink
      }
    })
  }

  // read (url: string) {
  read (url) {
    const headers = this.headers
    headers['content-type'] = 'application/json'
    return fetch(this.endpoint, {
      method: 'GET',
      headers
    }).then(response => {
      if (response.status === 200 || response.status === 201) {
        return response.json().then(data => {
          return data
        })
      }
    })
  }

  // update (url: string, operation: string, properties: object) {
  update (url, operation, properties) {
    const payload = { action: 'update', url }
    payload[operation] = properties
    // payload[operation][property] = values
    return fetch(this.endpoint, {
      method: 'POST',
      headers: {
        accept: 'application/json',
        authorization: `Bearer ${this.token}`,
        'content-type': 'application/json'
      },
      body: JSON.stringify(payload)
    }).then(response => {
      if (response.status === 200 || response.status === 201) {
        console.log('UPDATED!')
      }
    })
  }

  // delete (url: string) {
  delete (url) {
  }

  // query (q: string, args) {
  query (q, args) {
    return fetch(this.endpoint + `?q=${q}&search=${args}`, {
      headers: this.headers
    }).then(response => {
      if (response.status === 200 || response.status === 201) {
        return response.json().then(data => {
          return data
        })
      }
    })
  }

  upload () {
  }
}

/* ************************************************************* */

const appendAfter = (el, elAfter) => {
  el.parentNode.insertBefore(elAfter, el.nextSibling)
}

/* ************************************************************* */

window.onpopstate = function (e) {
  if (e.state === null) { return }
  console.log('popping', e.state)
  updateArticle(window.location, e.state.scroll)
}

export const updateArticle = (url, scroll) => {
  // XXX _("#loading")['el'].style.display = "block"
  const xhr = new XMLHttpRequest()
  xhr.open('GET', url)
  xhr.setRequestHeader('X-Chromeless', '1')
  xhr.onload = function () {
    executeUnloadScripts()

    const dom = new DOMParser().parseFromString(xhr.responseText, 'text/html')
    console.log(xhr.responseText)

    const newArticle = dom.querySelector('body > article')
    const currentArticle = _('article#content').el
    currentArticle.height = 0
    appendAfter(currentArticle, newArticle)
    currentArticle.remove()

    const newAside = dom.querySelector('body > div')
    const currentAside = _('aside div.page-related').el
    currentAside.height = 0
    appendAfter(currentAside, newAside)
    currentAside.remove()

    document.body.scrollTop = document.documentElement.scrollTop = scroll

    _('article#content a:not(.breakout)').each(upgradeLink)
    _('aside div.page-related a:not(.breakout)').each(upgradeLink)
    _('article#content script').each(el => {
      if (el.src !== '') {
        document.getElementsByTagName('head')[0].appendChild(el)
      } else {
        eval(el.innerHTML) // eslint-disable-line
      }
    })
    executeLoadScripts()
    upgradeTimestamps()
    // TODO bindWebActions()

    const h1 = newArticle.querySelector('h1')
    let title = '' // owner
    if (h1) { title = h1.textContent + '\u2009\u2014\u2009' + title }
    window.document.title = title
    // XXX _("#loading")['el'].style.display = "none"
  }
  /* xhr.onprogress = function() {
        // progress on transfers from the server to the client (downloads)
        function updateProgress (e) {
            console.log(e);
            if (e.lengthComputable) {
                var percentComplete = e.loaded / e.total * 100;
                debugSocket.send(percentComplete);
                // ...
            } else {
                // Unable to compute progress information since the total size is unknown
            }
        }
    } */
  xhr.timeout = 10000
  xhr.ontimeout = function () {
    // TODO exponential backoff?
    console.log(`Request for ${url} timed out. retrying..`)
    updateArticle(url, scroll)
  }
  xhr.send()
}

// TODO back button when coming back from different origin or same page hash

// const WEBACTION = true

export function upgradeLink (el) {
  const url = el.href
  // TODO if (url.indexOf("web+action") == 0) {  // web actions
  // TODO     el.addEventListener("click", (ev) => {
  // TODO         if (ev.ctrlKey)
  // TODO             return
  // TODO         // ev.preventDefault()
  // TODO         WEBACTION = true
  // TODO         return
  // TODO     });
  // TODO     return  // use native
  // TODO }
  if (url.indexOf(origin) === -1) { // different origin
    return // use native
  }
  if (url.indexOf('#') > -1) { // same origin, contains fragment identifier
    const urlParts = url.split('#')
    const currentUrlParts = window.location.href.split('#')
    if (urlParts[0] === currentUrlParts[0]) { // same page
      return // use native
    }
    // different page
    // XXX console.log(url_parts, current_url_parts);
  }
  el.addEventListener('click', (ev) => {
    if (ev.ctrlKey) { return }
    ev.preventDefault()
    go(url)
  })
}

export function go (url) {
  if ((url.startsWith('http://') || url.startsWith('https://')) &&
      !url.startsWith(window.location.origin)) {
    window.open(url, '_blank')
  } else {
    history.replaceState({ scroll: window.pageYOffset }, 'title', window.location.href)
    updateArticle(url, 0)
    history.pushState({ scroll: 0 }, 'title', url)
  }
}
