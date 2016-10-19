#!/usr/bin/php
<?php
@ob_end_clean();
/**
 * This commandline script outputs a list of tab-separated values,
 * with the name of country and the count of Tor exit nodes located in.
 *
 * Usage:
 *      ./torExitNodesByCountry.php > output_file.csv
 */

define('EXIT_NODES_URL', 'https://check.torproject.org/exit-addresses');

function getCountry($line)
{
    preg_match(
        '/^ExitAddress (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+/',
        $line,
        $matches
    );
    if (empty($matches))
    {
        return null;
    }
    $ip = $matches[1];
    return geoip_country_name_by_name($ip);
}

function incrementByCountry($country, $repository)
{
    if (isset($repository[$country]))
    {
        $repository[$country] ++;
    }
    else
    {
        $repository[$country] = 1;
    }
    return $repository;
}

$ipsByCountry = array();

$handle = fopen(EXIT_NODES_URL, "r");

if ($handle)
{
    while (($line = fgets($handle)) !== false)
    {
        if ($country = getCountry($line))
        {
            $ipsByCountry = incrementByCountry($country, $ipsByCountry);
        }
    }
    fclose($handle);
}

ksort($ipsByCountry);

foreach ($ipsByCountry as $country => $counter)
{
    printf("%s\t%s\n", $country, $counter);
}