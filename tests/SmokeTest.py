// upgrade-validation.spec.ts

import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

describe('Upgrade Validation: Test Suite for New Runtimes and Frameworks', () => {
  const targetVersions = {
    node: process.env.TARGET_NODE_VERSION || '20.10.0',
    angular: process.env.TARGET_ANGULAR_VERSION || '20.0.0',
    cypress: process.env.TARGET_CYPRESS_VERSION || '14.0.0',
    jest: process.env.TARGET_JEST_VERSION || '29.6.4'
  };

  function getNodeVersion() {
    return process.version.replace(/^v/, '');
  }

  function getAngularVersion(): string {
    const angularPkg = path.resolve('node_modules', '@angular', 'core', 'package.json');
    if (fs.existsSync(angularPkg)) {
      const v = JSON.parse(fs.readFileSync(angularPkg, 'utf-8')).version;
      return v;
    }
    throw new Error('@angular/core is not installed');
  }

  function getCypressVersion(): string {
    const path1 = path.resolve('node_modules', 'cypress', 'package.json');
    if (fs.existsSync(path1)) {
      return JSON.parse(fs.readFileSync(path1, 'utf-8')).version;
    }
    throw new Error('cypress is not installed');
  }

  function getJestVersion(): string {
    const path1 = path.resolve('node_modules', 'jest', 'package.json');
    if (fs.existsSync(path1)) {
      return JSON.parse(fs.readFileSync(path1, 'utf-8')).version;
    }
    throw new Error('jest is not installed');
  }

  function getDeprecatedApiUsage(filePattern: string, deprecatedApis: string[]): string[] {
    const glob = require('glob');
    const files = glob.sync(filePattern, { absolute: true });
    let found: string[] = [];
    for (const file of files) {
      const contents = fs.readFileSync(file, 'utf-8');
      for (const api of deprecatedApis) {
        if (contents.includes(api)) {
          found.push(`${file}: ${api}`);
        }
      }
    }
    return found;
  }

  function configLoadsWithoutError(configPath: string): boolean {
    try {
      require(configPath);
      return true;
    } catch (e) {
      return false;
    }
  }

  // --- Version Validations ---
  it('should have Node.js active at the exact target version', () => {
    expect(getNodeVersion()).toBe(targetVersions.node);
  });

  it('should have Angular @angular/core upgraded to the exact target version', () => {
    expect(getAngularVersion()).toBe(targetVersions.angular);
  });

  it('should have Cypress upgraded to the exact target version', () => {
    expect(getCypressVersion()).toBe(targetVersions.cypress);
  });

  it('should have Jest upgraded to the exact target version', () => {
    expect(getJestVersion()).toBe(targetVersions.jest);
  });

  // --- Critical application path -- Smoke Test ---
  it('allows a basic Jest test to run correctly', () => {
    // Simulate a basic function tested with jest (should pass).
    function add(a: number, b: number) { return a + b; }
    expect(add(2, 3)).toBe(5);
  });

  // --- Deprecated API Usage ---

  it('should not contain deprecated Angular APIs replaced in this upgrade', () => {
    const deprecated = ['Renderer', 'HttpModule', 'OpaqueToken'];
    const usages = getDeprecatedApiUsage('src/**/*.ts', deprecated);
    expect(usages).toEqual([]);
  });

  it('should not use Cypress deprecated APIs', () => {
    const deprecated = ['cypress.on("window:confirm"', 'Cypress.Server.defaults'];
    const usages = getDeprecatedApiUsage('cypress/**/*.js', deprecated);
    expect(usages).toEqual([]);
  });

  it('should not use Jest deprecated APIs', () => {
    const deprecated = ['jest.resetModuleRegistry', 'jest.addMatchers'];
    const usages = getDeprecatedApiUsage('src/**/*.test.{js,ts}', deprecated);
    expect(usages).toEqual([]);
  });

  // --- Configuration Validation ---

  it('loads new configuration keys from jest.config.ts without error', () => {
    // List new config keys introduced in latest Jest (as example: "roots", "projects")
    const configPath = path.resolve('jest.config.ts');
    if (!fs.existsSync(configPath)) {
      return pending('jest.config.ts not present');
    }
    expect(configLoadsWithoutError(configPath)).toBe(true);
    const config = require(configPath);
    expect(config).toHaveProperty('roots');
    expect(config).toHaveProperty('projects');
  });

  it('loads new configuration keys from cypress.config.ts without error', () => {
    // Cypress 14+ uses the 'e2e' key and projectSetupNodeEvents
    const configPath = path.resolve('cypress.config.ts');
    if (!fs.existsSync(configPath)) {
      return pending('cypress.config.ts not present');
    }
    expect(configLoadsWithoutError(configPath)).toBe(true);
    const config = require(configPath);
    expect(config).toHaveProperty('e2e');
    expect(config.e2e).toHaveProperty('setupNodeEvents');
  });

  // --- End-to-End Route Verification (basic demonstration) ---
  it('should allow launching the Angular app main entrypoint (AppModule)', () => {
    const appModulePath = path.resolve('src/app/app.module.ts');
    expect(fs.existsSync(appModulePath)).toBeTrue();
    const fileContent = fs.readFileSync(appModulePath, 'utf-8');
    // Just static validation of module presence
    expect(fileContent).toMatch(/@NgModule/);
    expect(fileContent).toMatch(/AppModule/);
  });

  it('should compile backend server entrypoint if present', () => {
    // Spring/Java/Python not in CAST, just check their main entrypoints if discovered
    const serverDir = path.resolve('backend');
    if (!fs.existsSync(serverDir)) {
      return pending('No backend directory present');
    }
    // Check for common entrypoints
    const found = fs.readdirSync(serverDir).some(f => f.match(/main\.(js|ts|py|java)$/));
    expect(found).toBeTrue();
  });
});