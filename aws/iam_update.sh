#!/usr/bin/env bash

function __confirm() {
    __ui_clear_stdin

    local message=$1
    local code=1

    case "${2}" in
        red)    code=31;;
        green)  code=32;;
        yellow) code=33;;
        blue)   code=34;;
        purple) code=35;;
        cyan)   code=36;;
        white)  code=37;;
        *)      code=1;;
    esac

    if [ $# -gt 1 ]; then
        local default=$2
    else
        local default=${FALSE}
    fi

    printf "\e[0;${code}m➜ Do you want to ${message}? \e[0m[y or n] "
    read -n 2
    echo -n
    if [[ $REPLY =~ ^[Yy] ]]; then
        return ${TRUE}
    else
        return ${FALSE}
    fi

    # Ctrl-D pressed.
    return ${default}
}

function __echo() {
    case "${2}" in
        red)    code=31;;
        green)  code=32;;
        yellow) code=33;;
        blue)   code=34;;
        purple) code=35;;
        cyan)   code=36;;
        white)  code=37;;
        *)      code=1;;
    esac
    printf "\e[0;${code}m${1}\e[0m\n"
}

function __notify() {
    __echo "➜ ${1}" "white"
}

function __uh_oh() {
    __echo "✖ ${1}" "red"
}

function __good() {
    __echo "✔ ${1}" "green"
}

function __update_group_policy() {
    local group_name=$1
    local policy_name=$2
    local policy_file="file://${3}"

    aws iam create-group --group-name "${group_name}" >> /dev/null 2>&1
    [ $? = 0 ] && __good "Created Group: ${group_name}"

    aws iam put-group-policy \
        --group-name "${group_name}" \
        --policy-name "${policy_name}" \
        --policy-document "${policy_file}"
        [ $? = 0 ] && __good "Success: ${group_name}:${policy_name}" \
        || __uh_oh "Failure: ${group_name}:${policy_name}"
}

function __update_role_policy() {
    local role_name=$1
    local policy_name=$2
    local policy_file="file://${3}"
    local trust_policy=$4

    roleData=$(aws iam list-roles)
    if [[ $roleData != *'"RoleName": "'${role_name}'"'* ]]
        then
            aws iam create-instance-profile \
            --instance-profile-name "${role_name}"
            [ $? = 0 ] && __good "Success: Created instance profile for ${role_name}" \
            || __uh_oh "Failure: Could not create instance profile ${role_name}"

            aws iam create-role --role-name "${role_name}" \
            --assume-role-policy-document "file://${trust_policy}"  >> /dev/null 2>&1
            [ $? = 0 ] && __good "Success: Created ${role_name}" \
            || __uh_oh "Failure: Could not create role ${role_name}"

            aws iam add-role-to-instance-profile \
            --instance-profile-name "${role_name}" \
            --role-name "${role_name}"
            [ $? = 0 ] && __good "Success: Added role to instance profile for ${role_name}" \
            || __uh_oh "Failure: Could not add role to instance profile for ${role_name}"
        fi

    aws iam put-role-policy \
    --role-name "${role_name}" \
    --policy-name "${policy_name}" \
    --policy-document "${policy_file}"
    [ $? = 0 ] && __good "Success: ${role_name}:policy ${policy_name}" \
    || __uh_oh "Failure: Could not add ${policy_name}"
}

function __update_trust_policy() {
    local trust_policy=$1

    aws iam update-assume-role-policy --role-name "${role_name}" \
    --policy-document "file://${trust_policy}"
    [ $? = 0 ] && __good "Success: Updated trust policy for ${role_name}" \
    || __uh_oh "Failure: Could not update trust policy for ${role_name}"
}

for group_path in $(find ./groups -maxdepth 1 -mindepth 1 -type d); do
    group_name=$(basename "${group_path}")
    __echo "Updating Group: ${group_name}..."
    for policy_path in $(find "${group_path}" \( -type f \) -or \( -type l \) -maxdepth 1); do
        policy_file=$(echo "${policy_path}" | sed 's/\.\///g')
        policy_name=$(basename "${policy_path}" | sed 's/\.json//g')
        __update_group_policy $group_name $policy_name $policy_file
    done
done

for role_path in $(find ./roles -maxdepth 1 -mindepth 1 -type d); do
    role_name=$(basename "${role_path}")
    __echo "Updating Role: ${role_name}..."
    trust_policy=${role_path}/trust/trust.json
    for policy_path in $(find "${role_path}" \( -type f \) -or \( -type l \) -maxdepth 1); do
        policy_file=$(echo "${policy_path}" | sed 's/\.\///g')
        policy_name=$(basename "${policy_path}" | sed 's/\.json//g')
        __update_role_policy $role_name $policy_name $policy_file $trust_policy
    done
    __update_trust_policy $trust_policy
done

