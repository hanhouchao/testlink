from xml.dom.minidom import parse


def readXML():
    domTree = parse("./ACP2.xml")
    root = domTree.documentElement
    testsuites = root.getElementsByTagName("testsuite")
    root.getElementsByTagName("testsuite")[0].getElementsByTagName("testsuite")[0].getElementsByTagName("testsuite")[1].getElementsByTagName("details")[
        0].childNodes[0].data
    root.getElementsByTagName("testsuite")[0].getElementsByTagName("testsuite")[0].getElementsByTagName("testsuite")[1].getAttribute("name")
    for testsuite in testsuites:
        testsuite.getElementsByTagName("testsuite")


def get_url(testsuites):
    for testsuite in testsuites:
        if len(testsuite.getElementsByTagName("testsuite")):
            root.getElementsByTagName("testsuite")[0].getElementsByTagName("testsuite")[0].getElementsByTagName("testsuite")[1].getElementsByTagName("details")[
                0].childNodes[0].data