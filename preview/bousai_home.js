/* Created: 2026-09-03 / homepage realtime behavior */
/* Updated: 2026-09-03 / direct JMA refresh with cached fallback */
(function () {
  var JMA = {
    quake: "https://www.jma.go.jp/bosai/quake/data/list.json",
    warning: "https://www.jma.go.jp/bosai/warning/data/r8/map.json",
    area: "https://www.jma.go.jp/bosai/common/const/area.json",
    typhoon: "https://www.jma.go.jp/bosai/typhoon/data/targetTc.json"
  };

  var WARNING_CODE_NAMES = {
    "02": "暴風雪警報",
    "03": "大雨警報",
    "04": "洪水警報",
    "05": "暴風警報",
    "06": "大雪警報",
    "07": "波浪警報",
    "08": "高潮警報",
    "32": "暴風雪特別警報",
    "33": "大雨特別警報",
    "35": "暴風特別警報",
    "36": "大雪特別警報",
    "37": "波浪特別警報",
    "38": "高潮特別警報",
    "43": "大雨危険警報"
  };

  function formatRealtimeDate(value) {
    if (!value) return "";
    var date = new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    return new Intl.DateTimeFormat("ja-JP", {
      month: "numeric",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    }).format(date);
  }

  function isRealtimeStale(value) {
    if (!value) return true;
    var date = new Date(value);
    if (Number.isNaN(date.getTime())) return true;
    return Date.now() - date.getTime() > 30 * 60 * 1000;
  }

  function normalizeIntensity(value) {
    var labels = {
      "5-": "5弱",
      "5+": "5強",
      "6-": "6弱",
      "6+": "6強"
    };
    return labels[value] || value;
  }

  function fetchJson(url) {
    return fetch(url + (url.indexOf("?") >= 0 ? "&" : "?") + "t=" + Date.now(), {
      cache: "no-store",
      mode: "cors"
    }).then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    });
  }

  function parseDirectEarthquake(reports) {
    if (!Array.isArray(reports)) return null;
    var report = reports.find(function (item) {
      return item && item.anm && item.maxi;
    }) || reports.find(function (item) {
      return item && item.anm;
    });
    if (!report) return null;
    return {
      title: report.ttl || "地震情報",
      time: report.at || report.rdt || null,
      area: report.anm || null,
      magnitude: report.mag || null,
      max_intensity: report.maxi ? normalizeIntensity(report.maxi) : null,
      headline: null,
      official_url: "https://www.jma.go.jp/bosai/map.html#contents=earthquake_map"
    };
  }

  function parseDirectWarnings(documents, areaData) {
    var class10s = areaData && areaData.class10s ? areaData.class10s : {};
    var state = {};
    if (!Array.isArray(documents)) {
      throw new Error("warning data is not an array");
    }

    documents.slice().sort(function (a, b) {
      var aa = a.reportDatetime || a.controlDatetime || "";
      var bb = b.reportDatetime || b.controlDatetime || "";
      return aa.localeCompare(bb);
    }).forEach(function (document) {
      var items = document && document.warning && Array.isArray(document.warning.class10Items)
        ? document.warning.class10Items
        : [];

      items.forEach(function (item) {
        var areaCode = String(item.areaCode || "");
        var areaName = class10s[areaCode] && class10s[areaCode].name
          ? class10s[areaCode].name
          : areaCode;

        (item.kinds || []).forEach(function (kind) {
          var code = String(kind.code || "");
          if (!WARNING_CODE_NAMES[code]) return;

          var key = areaName + "|" + code;
          var status = String(kind.status || "");
          if (
            status.indexOf("解除") >= 0 ||
            status.indexOf("取消") >= 0 ||
            status.indexOf("なし") >= 0
          ) {
            delete state[key];
            return;
          }
          state[key] = {
            area: areaName,
            kind: WARNING_CODE_NAMES[code]
          };
        });
      });
    });

    var grouped = {};
    Object.keys(state).forEach(function (key) {
      var item = state[key];
      if (!grouped[item.kind]) grouped[item.kind] = [];
      if (grouped[item.kind].indexOf(item.area) < 0) {
        grouped[item.kind].push(item.area);
      }
    });

    var groups = Object.keys(grouped).sort().map(function (kind) {
      var areas = grouped[kind].sort();
      return { kind: kind, areas: areas, count: areas.length };
    });

    return {
      active_count: Object.keys(state).length,
      groups: groups.slice(0, 8),
      official_url: "https://www.jma.go.jp/bosai/map.html#contents=warning"
    };
  }

  function parseDirectTyphoons(targetTcs) {
    if (!Array.isArray(targetTcs)) return [];
    return targetTcs.map(function (item) {
      return {
        event_id: item.tropicalCyclone || item.typhoonNumber || "",
        time: item.issue || null,
        title: item.typhoonNumber ? "台風等 " + item.typhoonNumber : "台風情報",
        active: true,
        official_url: "https://www.jma.go.jp/bosai/map.html#contents=typhoon"
      };
    });
  }

  function renderRealtimeEarthquake(root, data) {
    var main = root.querySelector("[data-realtime-earthquake]");
    var sub = root.querySelector("[data-realtime-earthquake-sub]");
    if (!main || !sub) return;

    var quake = data.earthquake;
    if (!quake) {
      main.textContent = "直近の地震情報を取得できていません。";
      sub.textContent = "";
      return;
    }

    var parts = [];
    if (quake.time) parts.push(formatRealtimeDate(quake.time));
    if (quake.area) parts.push(quake.area);
    if (quake.max_intensity) parts.push("最大震度" + quake.max_intensity);
    main.textContent = parts.join(" / ") || quake.title || "地震情報";

    var details = [];
    if (quake.magnitude) details.push("M" + quake.magnitude);
    if (quake.headline && !quake.max_intensity) details.push(quake.headline);
    sub.textContent = details.join("　");
  }

  function renderRealtimeWarnings(root, data) {
    var holder = root.querySelector("[data-realtime-warnings]");
    if (!holder) return;
    holder.textContent = "";

    var warnings = data.warnings;
    if (!warnings || typeof warnings !== "object") {
      var unavailable = document.createElement("p");
      unavailable.className = "realtime-none";
      unavailable.textContent = "警報・特別警報の情報を取得できていません。気象庁の公式情報を直接確認してください。";
      holder.appendChild(unavailable);
      return;
    }
    var groups = Array.isArray(warnings.groups) ? warnings.groups : [];
    if (!warnings.active_count || groups.length === 0) {
      var none = document.createElement("p");
      none.className = "realtime-none";
      none.textContent = "取得データでは、現在表示対象の警報・特別警報は確認されていません。";
      holder.appendChild(none);
      return;
    }

    var list = document.createElement("ul");
    list.className = "realtime-list";
    groups.forEach(function (group) {
      var item = document.createElement("li");
      var areas = Array.isArray(group.areas) ? group.areas : [];
      var visible = areas.slice(0, 3);
      var suffix = areas.length > 3 ? " ほか" + (areas.length - 3) + "地域" : "";
      item.textContent = group.kind + "：" + visible.join("、") + suffix;
      list.appendChild(item);
    });
    holder.appendChild(list);
  }

  function renderRealtimeTyphoons(root, data) {
    var holder = root.querySelector("[data-realtime-typhoon]");
    if (!holder) return;
    holder.textContent = "";

    var message = document.createElement("p");
    if (!Array.isArray(data.typhoons)) {
      message.className = "realtime-none";
      message.textContent = "台風情報を取得できていません。気象庁の公式情報を直接確認してください。";
      holder.appendChild(message);
      return;
    }
    var typhoons = data.typhoons;
    if (typhoons.length === 0) {
      message.className = "realtime-none";
      message.textContent = "現在、表示対象の台風・発達する熱帯低気圧は確認されていません。";
    } else {
      message.textContent = "現在、気象庁が台風等" + typhoons.length + "件を解析・予報しています。";
    }
    holder.appendChild(message);

    if (typhoons.length > 0) {
      var note = document.createElement("p");
      note.className = "realtime-card__sub";
      note.textContent = "進路・強度などの詳細は気象庁で確認してください。";
      holder.appendChild(note);
    }
  }

  function renderRealtimePanel(root, data) {
    var updated = root.querySelector("[data-realtime-updated]");
    var status = root.querySelector("[data-realtime-status]");
    var checkedAt = data.checked_at;
    var stale = isRealtimeStale(checkedAt);

    if (updated) {
      updated.textContent = checkedAt
        ? "最終取得 " + formatRealtimeDate(checkedAt)
        : "最終取得を確認できません";
    }

    renderRealtimeEarthquake(root, data);
    renderRealtimeWarnings(root, data);
    renderRealtimeTyphoons(root, data);

    if (status) {
      status.classList.remove("is-stale", "is-error");
      if (data.status === "degraded" || data.status === "partial") {
        status.classList.add("is-error");
        status.textContent = "一部の情報取得に失敗しています。表示内容が最新でない可能性があります。避難判断には気象庁・自治体などの最新情報を確認してください。";
      } else if (stale) {
        status.classList.add("is-stale");
        status.textContent = "情報更新が遅延している可能性があります。避難判断には気象庁・自治体などの最新情報を確認してください。";
      } else {
        status.textContent = data.note || "当サイトの表示には遅延する場合があります。避難判断には気象庁・自治体などの最新情報を確認してください。";
      }
    }
  }

  function refreshDirectFromJma(root, cached) {
    var quakeRequest = fetchJson(JMA.quake).then(parseDirectEarthquake);
    var warningRequest = Promise.all([
      fetchJson(JMA.warning),
      fetchJson(JMA.area)
    ]).then(function (values) {
      return parseDirectWarnings(values[0], values[1]);
    });
    var typhoonRequest = fetchJson(JMA.typhoon).then(parseDirectTyphoons);

    return Promise.allSettled([
      quakeRequest,
      warningRequest,
      typhoonRequest
    ]).then(function (results) {
      var data = Object.assign({}, cached || {});
      var successCount = 0;

      if (results[0].status === "fulfilled") {
        data.earthquake = results[0].value;
        successCount += 1;
      }
      if (results[1].status === "fulfilled") {
        data.warnings = results[1].value;
        successCount += 1;
      }
      if (results[2].status === "fulfilled") {
        data.typhoons = results[2].value;
        successCount += 1;
      }

      if (successCount === 0) return cached;

      // Do not make stale cached sections look freshly checked when only part of JMA refresh succeeds.
      if (successCount === 3) {
        data.checked_at = new Date().toISOString();
      }
      data.status = successCount === 3 ? "ok" : "partial";
      data.note = "気象庁の公開データを直接確認しています。表示には遅延する場合があるため、避難判断には気象庁・自治体などの最新情報を確認してください。";
      return data;
    });
  }

  function loadRealtimePanel(root) {
    fetch("realtime/realtime.json?t=" + Date.now(), { cache: "no-store" })
      .then(function (response) {
        if (!response.ok) throw new Error("HTTP " + response.status);
        return response.json();
      })
      .catch(function () {
        return {
          status: "degraded",
          checked_at: null,
          earthquake: null,
          warnings: null,
          typhoons: null
        };
      })
      .then(function (cached) {
        renderRealtimePanel(root, cached);
        return refreshDirectFromJma(root, cached);
      })
      .then(function (fresh) {
        if (fresh) renderRealtimePanel(root, fresh);
      })
      .catch(function () {
        var updated = root.querySelector("[data-realtime-updated]");
        var status = root.querySelector("[data-realtime-status]");
        if (updated) updated.textContent = "最新情報を取得できません";
        if (status) {
          status.classList.add("is-error");
          status.textContent = "防災情報を取得できませんでした。気象庁・自治体などの公式情報を直接確認してください。";
        }
      });
  }

  function initRealtimePanel() {
    var root = document.querySelector("[data-realtime-root]");
    if (!root) return;
    loadRealtimePanel(root);
    window.setInterval(function () {
      loadRealtimePanel(root);
    }, 10 * 60 * 1000);
  }

  function init() {
    initRealtimePanel();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
}());
