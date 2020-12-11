# -*- coding:utf-8 -*-
import sys

import testlink
import http.client
import xmlrpc.client
import ssl

import yaml

# python3 create_case.py <suite> case.yaml

url = 'http://testlink.alauda.cn/lib/api/xmlrpc/v1/xmlrpc.php'
key = '7ccbcfc2d1c580277d7b5ce1038c9ee6'
testproject_name = "ACP2 UI"
testproject_prefix = "ACP2UI"
suite = sys.argv[1]
case_path = sys.argv[2]


class ProxiedTransport(xmlrpc.client.Transport):
    def set_proxy(self, host, port=None, headers=None):
        self.proxy = host, port
        self.proxy_headers = headers
        self.contex = ssl._create_unverified_context()

    def make_connection(self, host):
        connection = http.client.HTTPSConnection(*self.proxy, context=self.contex)
        connection.set_tunnel(host)
        self._connection = host, connection
        return connection


proxy = ProxiedTransport()
proxy.set_proxy("139.186.2.80", 37491)

tlc = testlink.TestlinkAPIClient(url, key)


def create_test_case():
    testprojectid = tlc.getProjectIDByName(testproject_name)
    testsuiteid = get_suite_id(suite, testprojectid)
    with open(case_path, "r+") as fp:
        testcases = yaml.safe_load(fp.read())
        for (casename, casedetail) in testcases.items():
            importance = get_importance(casedetail["优先级"])
            if "步骤" in casedetail.keys():
                steps = refactor_steps(casedetail["步骤"])
            else:
                steps = []
            summary = casedetail.get("summary", "")
            try:
                tlc.getTestCaseIDByName(casename, testsuitename=suite, testprojectname=testproject_name)
                testcase_info = tlc.getTestCaseIDByName(casename, testsuitename=suite,
                                                        testprojectname=testproject_name)
                id = "{}-{}".format(testproject_prefix, testcase_info[0]["tc_external_id"])
                testcase_info = tlc.updateTestCase(testcaseexternalid=id, importance=importance, summary=summary,steps=steps)
                print(testcase_info)
                testcase_info = tlc.getTestCase(testcaseexternalid=id)
            except Exception as e:
                print(e)
                testcase_info = tlc.createTestCase(casename, testsuiteid, testprojectid, "hchan", summary, steps=steps, importance=importance)
            print(testcase_info)


def get_importance(importance):
    tmp = str(importance).lower()
    if tmp == "medium":
        return 2
    elif tmp == "low":
        return 1
    elif tmp == "high":
        return 0
    else:
        return 0


def refactor_steps(steps):
    data = []
    cnt = 0
    for step in steps:
        cnt += 1
        tmp_data = {}
        for actions, expected_results in step.items():
            if actions == "无":
                actions = ""
            if expected_results == "无":
                expected_results = ""
            tmp_data.update({"step_number": cnt, "actions": actions, "expected_results": expected_results, "execution_type": 0})
        data.append(tmp_data)
    return data


def get_suite_id(case_path, testprojectid):
    suite_id = ""
    suite = get_suite_info(case_path)
    if len(suite) > 0:
        suite_id = suite[0]["id"]
    elif suite_id:
        suite_id = tlc.createTestSuite(testprojectid, case_path, case_path, parentid=suite_id)[0]["id"]
    else:
        suite_id = tlc.createTestSuite(testprojectid, case_path, case_path)[0]["id"]
    return suite_id


def get_suite_info(path):
    suite = []
    try:
        suite = tlc.getTestSuite(path, testproject_prefix)
    except Exception as e:
        print(e)
    finally:
        return suite


if __name__ == "__main__":
    create_test_case()
