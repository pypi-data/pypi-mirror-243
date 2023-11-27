#!/usr/bin/env bash

get_boost(){
    BOOST=$(grep -m 1 "Boost version:" ./consoleText | sed  "s/.*-- Boost version: \([a-zA-Z0-9\.]*\)/\1/g")
    if [ -z "$BOOST" ]
    then
      BOOST=$(grep -m 1 "Found Boost:" ./consoleText | sed  "s/.*-- Found Boost:.*found suitable version \"\([a-zA-Z0-9\.]*\)\",.*/\1/g")
    fi
  echo "$BOOST"
}

get_compiler(){
    grep -m 1 "The C compiler identification" ./consoleText | sed  "s/.*-- The C compiler identification is \([a-zA-Z0-9\.]*\)/\1/g"
}

get_cmake(){
    grep -m 1 "Cmake version" ./consoleText| sed "s/.*-- Cmake version \([a-zA-Z0-9\.]*\)/\1/g"
}

get_eigen3(){
  sed -n 's/.* Eigen3 library \.\+: \([^ ]*\) in .*/\1/p;T;q' ./consoleText
}

get_json(){
  sed -n 's/.* JSON library \.\+: \([^ ]*\) in .*/\1/p;T;q' ./consoleText
}

get_ns3(){
  sed -n 's/.*-- ns-3 found (v\(3[-.0-9a-z]\+\).*/\1/p;T;q' ./consoleText
}

get_python(){
  found=$(grep -c "Compile Python bindings .....: ON" ./consoleText)
  if [ "$found" != 0 ]; then
    grep -m 1 "Found Python3" ./consoleText| sed "s/.*-- Found Python3.*found version \"\([a-zA-Z0-9\.]*\)\".*/\1/g"
  else
    echo ""
  fi
}

if [ -f consoleText ]; then
  rm consoleText
fi


if [ -z "$BUILD_URL" ]; then
  BUILD_URL="https://ci.inria.fr/simgrid/job/SimGrid/lastBuild"
fi

#get the list of nodes on jenkins
wget --quiet ${BUILD_URL}/consoleText >/dev/null 2>&1
nodes=($(sed -n 's/^Triggering SimGrid [^ ]* Debug,//p' ./consoleText| sort))
rm consoleText

cat <<EOF
<br>Description of the nodes - Automatically updated by project_description.sh script - Don't edit here<br><br>
<script>
function compareVersion(v1, v2) {
    if (typeof v1 !== 'string') return false;
    if (typeof v2 !== 'string') return false;
    v1 = v1.split('.');
    v2 = v2.split('.');
    const k = Math.min(v1.length, v2.length);
    for (let i = 0; i < k; ++ i) {
        v1[i] = parseInt(v1[i], 10);
        v2[i] = parseInt(v2[i], 10);
        if (v1[i] > v2[i]) return 1;
        if (v1[i] < v2[i]) return -1;
    }
    return v1.length == v2.length ? 0: (v1.length < v2.length ? -1 : 1);
}</script>
<script>
function sortTable(n, type) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById('configuration-matrix');
  switching = true;
  //Set the sorting direction to ascending:
  dir = 'asc';
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName('TD')[n];
      y = rows[i + 1].getElementsByTagName('TD')[n];
      /*check if the two rows should switch place,
      based on the direction, asc or desc:*/
      if (dir == 'asc') {
        if(type == 'version'){
          shouldSwitch = (compareVersion(x.innerHTML.toLowerCase(), y.innerHTML.toLowerCase()) > 0);
        }else{
          shouldSwitch = (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase());
        }
      } else if (dir == 'desc') {
        if(type == 'version'){
          shouldSwitch = (compareVersion(x.innerHTML.toLowerCase(), y.innerHTML.toLowerCase()) < 0);
        }else{
          shouldSwitch = (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase());
        }
      }
      if (shouldSwitch)
        break;
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /*If no switching has been done AND the direction is 'asc',
      set the direction to 'desc' and run the while loop again.*/
      if (switchcount == 0 && dir == 'asc') {
        dir = 'desc';
        switching = true;
      }
    }
  }
}
</script>
<table id=configuration-matrix>
  <tr class=matrix-row>
    <td class=matrix-header style=min-width:75px onclick='sortTable($((col=0)));'>Name of the Builder</td>
    <td class=matrix-header style=min-width:75px onclick='sortTable($((++col)));'>OS</td>
    <td class=matrix-header style=min-width:50px onclick='sortTable($((++col,0)));'>Debug</td>
    <td class=matrix-header style=min-width:50px onclick='sortTable($((++col,0)));'>MC</td>
    <td class=matrix-header style=min-width:75px onclick='sortTable($((++col)));'>Compiler</td>
    <td class=matrix-header style=min-width:75px onclick="sortTable($((++col)),'version');">Boost</td>
    <td class=matrix-header style=min-width:75px onclick="sortTable($((++col)),'version');">Cmake</td>
    <td class=matrix-header style=min-width:50px onclick="sortTable($((++col)),'version');">Eigen3</td>
    <td class=matrix-header style=min-width:50px onclick="sortTable($((++col)),'version');">JSON</td>
    <td class=matrix-header style=min-width:50px onclick="sortTable($((++col)),'version');">ns-3</td>
    <td class=matrix-header style=min-width:50px onclick="sortTable($((++col)),'version');">Python</td>
  </tr>
EOF

declare -A icons
icons=(
    [success]="img src=https://ci.inria.fr/simgrid/images/24x24/blue.png"
    [failure]="img src=https://ci.inria.fr/simgrid/images/24x24/red.png"
    [disabled]="img src=https://ci.inria.fr/simgrid/images/24x24/disabled.png"
)

for node in "${nodes[@]}"
do
    wget --quiet --output-document=consoleText \
         ${BUILD_URL}/build_mode=Debug,node=${node}/consoleText \
         ${BUILD_URL}/build_mode=ModelChecker,node=${node}/consoleText \
         >/dev/null 2>&1
    if [ ! -f consoleText ]; then
      echo "file not existing for node ${node}"
      exit 1
    fi
    boost=$(get_boost)
    compiler=$(get_compiler)
    cmake=$(get_cmake)
    eigen3=$(get_eigen3)
    json=$(get_json)
    ns3=$(get_ns3)
    py=$(get_python)
    os=$(grep -m 1 "OS Version" ./consoleText| sed "s/OS Version : \(.*\)/\1/g")

    color1=""
    color2=""
    #in case of success, replace blue by green in status balls
    wget --quiet https://ci.inria.fr/simgrid/buildStatus/text?job=SimGrid%2Fbuild_mode%3DDebug%2Cnode%3D"${node}" -O status  >/dev/null 2>&1

    status=$(cat status)
    if [ "$status" == "Success" ]; then
      color1="&color=green"
    fi
    rm status
    statusdebug="<a href=\"build_mode=Debug,node=${node}/\"><img src=\"https://ci.inria.fr/simgrid/job/SimGrid/build_mode=Debug,node=${node}/badge/icon?style=ball-24x24${color1}\"/>"

    statusmc="<${icons[disabled]}>"
    wget --quiet https://ci.inria.fr/simgrid/buildStatus/text?job=SimGrid%2Fbuild_mode%3DModelChecker%2Cnode%3D"${node}" -O status >/dev/null 2>&1
    status=$(cat status)
    if [ "$status" ]; then
      if [ "$status" == "Success" ]; then
        color2="&color=green"
      fi
      statusmc="<a href=\"build_mode=ModelChecker,node=${node}/\"><img src=\"https://ci.inria.fr/simgrid/job/SimGrid/build_mode=ModelChecker,node=${node}/badge/icon?style=ball-24x24${color2}\"/>"
    fi
    rm status

    cat <<EOF
  <tr>
    <td class="matrix-leftcolumn">$node</td>
    <td class="matrix-cell" style="text-align:left">$os</td>
    <td class="matrix-cell" style="text-align:center">${statusdebug}</td>
    <td class="matrix-cell" style="text-align:center">${statusmc}</td>
    <td class="matrix-cell" style="text-align:left">$compiler</td>
    <td class="matrix-cell" style="text-align:left">$boost</td>
    <td class="matrix-cell" style="text-align:left">$cmake</td>
    <td class="matrix-cell" style="text-align:center">$eigen3</td>
    <td class="matrix-cell" style="text-align:center">$json</td>
    <td class="matrix-cell" style="text-align:left">$ns3</td>
    <td class="matrix-cell" style="text-align:left">$py</td>
  </tr>
EOF
    rm consoleText
done

echo "</table>"
