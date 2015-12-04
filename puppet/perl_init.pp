#Perl class with installCPAN define type for installing perl modules
class perl {

  define installCPAN () {
    exec { "cpanLoad${title}":
      command => "cpanm ${name}",
      path    => '/usr/bin:/usr/sbin:/bin:/sbin:/usr/local/bin',
      unless  => "perl -I.cpan -M${title} -e 1",
      timeout => 600,
      require => exec['initCPAN'],
    }
  }

  package { 'perl': ensure => installed }

  exec { 'initCPAN':
    command => 'wget -O - http://cpanmin.us | perl - --self-upgrade',
    path    => '/usr/bin:/usr/sbin:/bin:/sbin',
    creates => '/usr/bin/cpanm',
    require => Package['perl']
  }

}
