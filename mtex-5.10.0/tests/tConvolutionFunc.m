% Copyright 2023 The MathWorks, Inc.

% Any test normally can be divided in following
% steps:
% 1. Set up - setting up environment for test
% 2. Action - Execute source code which we intend to test
% 3. Verification - Verify output of execution with expected
%                   value
% 4. Teardown - Clean up environment so next test starts fresh

function tests = tConvolutionFunc
% This is a standard function for function based MATLAB tests. Used for
% identifying tests in the file
tests = functiontests(localfunctions);
end

function teardown(~)
% Teardown for each test. Each test method should start in a clean
% test environment (For eg. No variables in base workspace.) Code
% placed in this section is executed at the end of each test method
% below.

figHandles = findall(groot,'Type','figure');
close(figHandles, "force");
end

function testS2Kernels(testCase)
% Import plugins from matlab.unittest package over here:
% Diagnostic: Can be imported from matlab.unittest.diagnostics.
%             Used for adding diagnostics/debug information in tests
%             More details can be found here:
% https://www.mathworks.com/help/matlab/ref/matlab.automation.diagnostics.diagnostic-class.html
% Fixtures: Can be imported from matlab.unittest.fixtures.
%           Fixtures are used for setting test environment, like creating
%           temp folders, setting up user path, etc.
%           More details can be found here:
%           https://www.mathworks.com/help/matlab/ref/matlab.unittest.fixtures-package.html

import matlab.unittest.diagnostics.Diagnostic;
import matlab.unittest.diagnostics.FigureDiagnostic;
import matlab.unittest.constraints.IsEqualTo
import matlab.unittest.constraints.RelativeTolerance

rng('default')

psi = S2DeLaValleePoussinKernel(10);

% Plots should not be used as method of comparison as it is
% difficult to compare plots to an expected value. Plots could
% be used as diagnostics for getting more details about test
% failures or detailed analysis

plot(psi)
figHandleHarmonic = figure(1);
F1 = S2FunHarmonic(psi);
plot(F1)
testCase.log(3, Diagnostic.join('Please verify plots', ...
    FigureDiagnostic(figHandleHarmonic)));

F2 = S2FunHandle( @(v) psi.eval(cos(angle(vector3d.Z,v))) );
figHandleS2Fun = figure(2);
plot(F2)

% Diagnotics for analyzing the test results. This will also be
% added to the generated test reports.
testCase.log(3, Diagnostic.join('Please verify plots', ...
    FigureDiagnostic(figHandleS2Fun)));

v=vector3d.rand;

% This is verification part of the test. This decides if test
% will fail or pass. Without this there part reliability of
% test can be questioned.

testCase.verifyThat(F1.eval(v),IsEqualTo(F2.eval(v), ...
    "Within",RelativeTolerance(1^-3)), "Values do not match for S2FunHarmonic and S2FunHandle");

end

function testSO3Kernels(testCase)

% Import plugins from matlab.unittest package over here:
% Diagnostic: Can be imported from matlab.unittest.diagnostics.
%             Used for adding diagnostics/debug information in tests
%             More details can be found here:
% https://www.mathworks.com/help/matlab/ref/matlab.automation.diagnostics.diagnostic-class.html
% Fixtures: Can be imported from matlab.unittest.fixtures.
%           Fixtures are used for setting test environment, like creating
%           temp folders, setting up user path, etc.
%           More details can be found here:
%           https://www.mathworks.com/help/matlab/ref/matlab.unittest.fixtures-package.html

import matlab.unittest.diagnostics.Diagnostic;
import matlab.unittest.diagnostics.FigureDiagnostic;
import matlab.unittest.constraints.IsEqualTo
import matlab.unittest.constraints.RelativeTolerance

rng(4)
psi = SO3DeLaValleePoussinKernel(4);

% Plots should not be used as method of comparison as it is
% difficult to compare plots to an expected value. Plots could
% be used as diagnostics for getting more details about test
% failures or detailed analysis

figHandleHarmonic = figure(1);
F1 = SO3FunHarmonic(psi);
plot(F1)

testCase.log(3, Diagnostic.join('Please verify plots', ...
    FigureDiagnostic(figHandleHarmonic)));

F2 = SO3FunHandle( @(rot) psi.eval(cos(angle(rot)/2)) );
figHandleS2Fun = figure(2);
plot(F2)

% Diagnotics for analyzing the test results. This will also be
% added to the generated test reports.

testCase.log(3, Diagnostic.join('Please verify plots', ...
    FigureDiagnostic(figHandleS2Fun)));

r = rotation.rand;

% This is verification part of the test. This decides if test
% will fail or pass. Without this there part reliability of
% test can be questioned.

testCase.verifyThat(F1.eval(r),IsEqualTo(F2.eval(r), ...
    "Within",RelativeTolerance(1^-3)), "Values do not match for S2FunHarmonic and S2FunHandle");
end

function testconvolutionSO3FunWithSO3Fun(testCase)

% Multiple verifications can be done in same test. In this test
% we are performing multiple actions and comparing results to
% expected values.

% convolution SO3Fun with SO3Fun
% Left sided (*L) and Right sided (*R) works
import matlab.unittest.constraints.IsEqualTo
import matlab.unittest.constraints.RelativeTolerance

rng('default')

F1 = SO3FunHarmonic(rand(1e3,1),crystalSymmetry('1'),specimenSymmetry('3'));
F2 = SO3FunHarmonic(rand(1e2,1),crystalSymmetry('4'),specimenSymmetry('1'));
r = rotation.rand;

% Left sided convolution
C=conv(F1,F2);

% Verification 1. RelTol is used for comparing
% C.eval(r), mean(SO3FunHandle(@(rot) (x) and
% F1.eval(rot).*F2.eval(inv(rot).*r))) (y). relTol can be
% considered as acceptable error in this case. If x~=y test
% will fail and a diagnostic will be thrown "Values do not
% match" . More verbose and meaningful diagnostics should be
% added which makes debugging and understanding of tests
% easier.

testCase.verifyThat(C.eval(r),IsEqualTo(mean(SO3FunHandle(@(rot) F1.eval(rot).*F2.eval(inv(rot).*r))), ...
    "Within",RelativeTolerance(1^-3)), "Values do not match");


% calcMDF
F1 = SO3FunHarmonic(rand(1e3,1),crystalSymmetry('3'),specimenSymmetry('1'));
F1.fhat = conj(F1.fhat);
C = conv(inv(conj(F1)),F2);
cF1 = conj(F1);

testCase.verifyThat(C.eval(r),IsEqualTo(mean(SO3FunHandle(@(rot) cF1.eval(rot).*F2.eval(rot.*r))), ...
    "Within",RelativeTolerance(1^-3)), "Values do not match");


% right sided convolution
F1 = SO3FunHarmonic(rand(1e3,1),crystalSymmetry('4'),specimenSymmetry('622'));
F2 = SO3FunHarmonic(rand(1e2,1),crystalSymmetry('622'),specimenSymmetry('3'));
C = conv(F1,F2,'Right');

% Verification 2.
testCase.verifyThat(C.eval(r),IsEqualTo(mean(SO3FunHandle(@(rot) F1.eval(rot).*F2.eval(r.*inv(rot)))), ...
    "Within",RelativeTolerance(1^-3)), "Values do not match");


end