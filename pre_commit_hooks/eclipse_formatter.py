from __future__ import print_function

import argparse
import subprocess
import os
import errno
import pkg_resources


def create_pom(pom_file, args):
    if not os.path.exists(os.path.dirname(pom_file)):
        try:
            os.makedirs(os.path.dirname(pom_file))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    version = pkg_resources.require("pre_commit_hooks")[0].version
    with open(pom_file, 'w') as f:
        f.write("""<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>se.extenda.maven</groupId>
  <artifactId>eclipse-formatter</artifactId>
  <version>{version}</version>
  <build>
    <directory>.</directory>
    <plugins>
      <plugin>
        <groupId>net.revelc.code.formatter</groupId>
        <artifactId>formatter-maven-plugin</artifactId>
        <version>2.7.0</version>
        <configuration>
          <directories>
            <directory>../../</directory>
          </directories>
          <compilerCompliance>{source}</compilerCompliance>
          <compilerSource>{source}</compilerSource>
          <compilerTargetPlatform>{target}</compilerTargetPlatform>
          <lineEnding>LF</lineEnding>
          <encoding>UTF-8</encoding>
          <useEclipseDefaults>true</useEclipseDefaults>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
""".format(source=args.source, target=args.target, version=version))


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*',
                        help='Java filenames to check.')
    parser.add_argument('--source', default='1.8', help='Java source version.')
    parser.add_argument('--target', default='1.8', help='Java target version.')
    args = parser.parse_args(argv)

    pom_file = 'target/.eclipse-formatter/formatter-pom.xml'
    create_pom(pom_file, args)

    includes = ','.join(args.filenames)

    env = os.environ.copy()
    env['MAVEN_OPTS'] = (
        '-Dorg.slf4j.simpleLogger.defaultLogLevel=error ' +
        '-Dorg.slf4j.simpleLogger.log.net.revelc.code.formatter=info'
    )

    status = subprocess.call([
        'mvn', '-B', '-f', pom_file,
        'formatter:format',
        '-Dformatter.includes=' + includes
    ], env=env)

    os.remove(pom_file)
    return status


if __name__ == '__main__':
    exit(main())
