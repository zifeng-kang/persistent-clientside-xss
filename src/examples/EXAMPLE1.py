# Copyright (C) 2019 Ben Stock & Marius Steffens
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# flow from document.cookie into a DOM sink
EXAMPLE1 = {
    "finding_id": 1,
    # DOM sink
    "sink_id": 3,
    # all the non-fix source i.e. source!=0
    # in this case it is only one entry originating from document.cookie
    "sources": [
        {
            # the associated finding
            "finding_id": 1,
            "id": 1337,
            # the associated source ID, in this case document.cookie
            "source": 8,
            # character offset in the complete value which ended up in the sink
            "start": 155,
            "end": 177,
            # value which originates from document.cookie and ends up being used in the context of the DOM sink
            "value_part": "pl346262568.1222667869",
            "source_name": "document.cookie",
            # flags indicating whether the respective encoding functions were used
            "hasEscaping": 0,
            "hasEncodingURI": 0,
            "hasEncodingURIComponent": 0
        }
    ],
    # the url associated with the frame in which the flow was found
    "url": "https://foo.com/",
    # the relevant storage entries of the frame in which the flow was found, in this case only cookies were found
    "storage": {
        "cookies": [
            [
                "vuid",
                "pl346262568.1222667869",
                -1
            ],
            [
                "_bpsid",
                "9cd8a3c6-6443-40b5-8242-1e781265ce6c",
                -1
            ],
            [
                "_gcl_au",
                "1.1.2072442439.1552320678",
                -1
            ],
            [
                "_ga",
                "GA1.2.957904215.1552320679",
                -1
            ],
            [
                "_gid",
                "GA1.2.1810131797.1552320679",
                -1
            ],
            [
                "_gat_UA-76641-8",
                "1",
                -1
            ],
            [
                "__qca",
                "P0-1774441245-1552320679695",
                -1
            ],
            [
                "_fbp",
                "fb.1.1552320679910.1251931420",
                -1
            ],
            [
                "__ssid",
                "cef8f18b-670c-4c33-81f5-621de5f0e744",
                -1
            ]
        ],
        "storage": []
    },
    # complete value which ended up in the sink
    "value": "A<div>\n     <script type=\"text/gtmscript\">var MathTag={version:\"1.0\",previous_url:document.referrer,industry:\"internet services\",mt_adid:\"182258\",mt_exem:\"pl346262568.1222667869\",event_type:\"home\",mt_id:\"1137909\",page_name:\"\\/\",client_status:\"none\"};</script>\n     <script type=\"text/gtmscript\" data-gtmsrc=\"//pixel.mathtag.com/event/js?mt_pp=1&amp;mt_adid=182258&amp;mt_id=1137909\"></script>\n</div>",
    # additional information as generated by our tainted chromium engine
    "d1": "innerHTML",
    "d2": "div",
    "d3": ""
}
