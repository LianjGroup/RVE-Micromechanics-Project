% Copyright 2023 The MathWorks, Inc.

%% Running test suite/ Multiple tests
% Import test report plugin
import matlab.unittest.plugins.TestReportPlugin;


% Create a test runner which
runner = matlab.unittest.TestRunner.withTextOutput;
runner.addPlugin(TestReportPlugin.producingHTML('Verbosity',3))

% Create testsuite a test suite for tests to run

suite = testsuite({'tConvolutionFunc.m'});

% Run tests
runner.run(suite)

%% Running individual tests
% The above code runs all tests mentioned in the suite, if you want to run
% individual tests use runtests. 
%
% For running complete test file use:
% >> runtests("tConvolutionFunc")
% For running specific test point in test file use:
% >> runtests("tConvolutionFunc","ProcedureName","testS2Kernels")
%
% The above commands will run the test and print results on Command prompt.
% This should be used either for verifying if the test is working or if you
% need a quick qualification using a single test.
