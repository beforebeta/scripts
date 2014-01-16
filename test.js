document.addEventListener("DOMContentLoaded", function () {
    CheckRTL();
    InitSeoStats()
});
function CheckRTL() {
    IsRTL() && (document.body.style.direction = "rtl")
}
function InitSeoStats() {
    PageRank_ShowItems();
    OnCheckSelectedTab()
}
function PageRank_ShowItems() {
    var a = '<table id="table_2cols"><tr><td class="top col">', b = GetLink("a_addtosite", MYLANG("AddTo"), MYLANG("PrPlugin") + ": " + MYLANG("AddTo"), "", "", 0), a = a + GetReportHead(MYLANG("Rank"), "rank"), a = a + (GetReportItem("rank_alexa", 0) + GetReportItem("rank_compete", 2) + GetReportItem("rank_ggpr", 3)), a = a + ('<tr class="tr_b"><td class="td_1" title="' + MYLANG("AddTo") + '"><div id="img_addpr" class="imgicon"></div></td><td colspan=2 id="add_pr"><div id="add_pr_txt">' + b + "</div></td></tr>"), a =
        a + GetReportTail(), a = a + '<div class="report_space"></div>' + GetGroupItems({"0": "ch_archive", 1: "ch_google"}, "Cache", "cache", 0), a = a + '<div class="report_space"></div>', a = a + GetGroupItems({"0": "bl_alexa", 1: "bl_google_w", 2: "bl_ose", 3: "bl_sogou", 4: "", 5: ""}, "Backlinks", "backlinks", 0), a = a + '</td><td class="top space"></td><td class="top col">', a = a + GetGroupItems({"0": "idx_ask", 1: "idx_baidu", 2: "idx_bing", 3: "idx_goo", 4: "idx_google", 5: "idx_sogou", 6: "idx_soso", 7: "idx_yahoo", 8: "idx_yandex", 9: "idx_360"}, "PagesIndexed",
        "indexed", 0), a = a + '<div class="report_space2"></div>', a = a + GetGroupItems({"0": "geoip_ip2", 1: "geoip_city2", 2: "geoip_country2"}, "GeoLocation", "geoip", 0), a = a + "</td></tr></table>";
    $("#content").html(a);
    $("#lnk_rank_ggpr").html(GetLink("a_rank_ggpr", MYLANG("GooglePR"), MYLANG("CheckOnline"), "", "", 0));
    SetLinkActions({a_addtosite: {type: "link", sel: 1, url: "http://pagerank.chromefans.org/pagerank-button/?ref=ext_pr"}, a_rank_ggpr: {type: "link", sel: 1, url: "http://pagerank.chromefans.org/?ref=ext_pr"}})
}
function OnCheckSelectedTab() {
    if ("" != sessionStorage.url) {
        for (var a in g_arrSites)"seostats" == g_arrSites[a].tab && AjaxUpdate(a, 0);
        CheckAlexaReady();
        CheckCompeteReady();
        CheckGeoipReady();
        "" != sessionStorage.url && ($("#geoip_ip").html('<img src="image/loading.gif" class="icon_16" ALT="">'), $("#geoip_city").html('<img src="image/loading.gif" class="icon_16" ALT="">'))
    }
}
function CheckCompeteReady() {
    if (void 0 == sessionStorage.remote_tf_compete && (void 0 == sessionStorage.cache_tf_compete || "" == sessionStorage.cache_tf_compete))setTimeout(CheckCompeteReady, 1E3); else {
        var a = void 0 == sessionStorage.remote_tf_compete ? sessionStorage.cache_tf_compete : sessionStorage.remote_tf_compete, a = -1 == a ? MYLANG("Unranked") : a;
        UpdateEndResult("rank_compete", a, MYLANG("site_compete") + ": " + a + "\r\n" + MYLANG("ClickMore"))
    }
}
function CheckAlexaReady() {
    if (void 0 == sessionStorage.remote_tf_alexa && (void 0 == sessionStorage.cache_tf_alexa || "" == sessionStorage.cache_tf_alexa))setTimeout(CheckAlexaReady, 1E3); else {
        var a = void 0 == sessionStorage.remote_tf_alexa ? "cache_" : "remote_", b = -1 == sessionStorage[a + "bl_alexa"] ? MYLANG("NA") : FixVal(sessionStorage[a + "bl_alexa"], 0, 1);
        UpdateEndResult("bl_alexa", b, MYLANG("NumLink") + "\r\n" + MYLANG("MoreLink"));
        a = -1 == sessionStorage[a + "tf_alexa"] ? MYLANG("Unranked") : sessionStorage[a + "tf_alexa"];
        UpdateEndResult("rank_alexa",
            a, MYLANG("AlexaRank") + ": " + a + "\r\n" + MYLANG("ClickMore"))
    }
}
function CheckGeoipReady() {
    if (void 0 == sessionStorage.remote_geoip_ip && (void 0 == sessionStorage.cache_geoip_ip || "" == sessionStorage.cache_geoip_ip))setTimeout(CheckGeoipReady, 1E3); else {
        var a = void 0 == sessionStorage.remote_geoip_ip ? "cache_" : "remote_";
        if ("" == sessionStorage[a + "geoip_ip"])a = MYLANG("NA"), $("#geoip_ip2").html(a), $("#geoip_city2").html(a), $("#geoip_country2").html(a); else {
            var b = "http://" + (void 0 == sessionStorage[a + "geoip_subdomain"] ? "www" : sessionStorage[a + "geoip_subdomain"]) + ".geoipview.com/?ref=ext_pr_home&q=" +
                sessionStorage[a + "geoip_ip"], d = MYLANG("ClickMore");
            OutputLink("geoip_ip2", "link", 0, MYLANG("ip"), "", "loading.gif", "icon_16", b);
            OutputLink("geoip_city2", "link", 0, MYLANG("City"), "", "loading.gif", "icon_16", b);
            OutputLink("geoip_country2", "link", 0, MYLANG("Country"), "", "loading.gif", "icon_16", b);
            b = MYLANG("IP") + ": " + sessionStorage[a + "geoip_ip"] + "\r\n" + MYLANG("City") + ": " + sessionStorage[a + "geoip_city"] + "\r\n" + MYLANG("Country") + ": " + sessionStorage[a + "geoip_country"] + "\r\n" + d;
            UpdateEndResult("geoip_ip2", sessionStorage[a +
                "geoip_ip"], b);
            UpdateEndResult("geoip_city2", sessionStorage[a + "geoip_city"], b);
            UpdateEndResult("geoip_country2", sessionStorage[a + "geoip_country"] + ' <img src="image/flags/' + sessionStorage[a + "geoip_code"] + '.png" class="icon_flag" ALT="' + sessionStorage[a + "geoip_country"] + '">', b)
        }
    }
};
function GetGroupItems(a, b, d, e) {
    var c = "", f = 0, h = 0, g = "", i;
    for (i in a)0 < f && e && (c += '</table><table id="tbl_' + d + f + '" class="report_tbl">'), g = GetReportItem(a[i], h), "" != g && h++, c += g, f++;
    "" != c && (c = GetReportHead(MYLANG(b), d) + c + GetReportTail());
    return c
}
function GetReportHead(a, b) {
    return'<div id="h_' + b + '" class="report_title"><div class="report_title_txt">' + a + '</div></DIV><div class="report_items"><table id="tbl_' + b + '" class="report_tbl">'
}
function GetReportTail() {
    return"</table></div>"
}
function GetReportItem(a, b) {
    if ("" == a)return'<tr class="' + (0 == b ? "noborder " : "") + (b % 2 ? "tr_b" : "tr_a") + '"><td colspan=3></td></tr>';
    if (!g_arrSites[a])return"";
    var d = g_arrSites[a], e = "td_2", c = "td_3";
    "rank_ggpr" == a || "rank_alexa" == a || "rank_compete" == a ? (e = "td_2_gg", c = "td_3_gg") : "domain_dns" == a || "domain_dns2" == a || "geoip_ip2" == a || "geoip_city2" == a || "geoip_ip" == a || "geoip_city" == a || "geoip_country" == a || "geoip_country2" == a ? (e = "td_2_ip", c = "td_3_ip") : "ch_google" == a || "ch_archive" == a ? (e = "td_2_ch", c = "td_3_ch") : "traffic" ==
        g_arrSites[a].tab && (e = "td_2_tf", c = "td_3_tf");
    var f = MYLANG(d.text_id), d = "" == d.tip_id ? f : f + "(" + MYLANG(d.tip_id) + ")";
    return'<tr class="' + (0 == b ? "noborder " : "") + (b % 2 ? "tr_b" : "tr_a") + '" id="tr_' + a + '">    <td class="td_1" title="' + d + '"><div id="img_' + a + '" class="imgicon"></div></td>    <td class="' + e + '" title="' + d + '"><div class="' + e + '_txt" id="lnk_' + a + '" >' + f + '</div></td>    <td class="' + c + '" id="val_' + a + '"><div id="' + a + '" class="' + c + '_txt" ></div></td>    </tr>'
};
