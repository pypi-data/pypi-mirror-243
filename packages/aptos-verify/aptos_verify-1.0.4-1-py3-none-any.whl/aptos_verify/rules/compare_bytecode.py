# This rule will check code that public onchain with current bytecode of one module_id
from aptos_verify.utils import AptosRpcUtils, AptosBytecodeUtils, AptosModuleUtils
from aptos_verify.schemas import OutputResult, VerifyArgs
from aptos_verify.config import Config, get_logger, get_config
from aptos_verify.exceptions import ModuleNotFoundException
import asyncio
from aptos_verify.decorators import config_rule
import aptos_verify.exceptions as verify_exceptions
import time
import os

logger = get_logger(__name__)


async def get_bytecode_from_source_code_onchain(move_build_path: str,
                                                params: VerifyArgs,
                                                ):
    """
    Get source code onchain and build by a Move Template.
    """
    import tomli_w
    import tomli
    # get source code onchain
    module_data = await AptosRpcUtils.rpc_account_get_source_code(params)

    account_address = params.account_address
    module_name = params.module_name

    flat_modules = [module_data.get('module')] + \
        module_data.get('related_modules')

    merge_source_code_string = ""
    parsing_manifest = None
    for source_code in flat_modules:
        bytecode = source_code.get('source')
        if not bytecode or bytecode.replace('0x', '') == '':
            raise verify_exceptions.ModuleHasNoSourceCodeOnChainException()
        package = source_code.get('package')
        decompressed_source_code = AptosBytecodeUtils.decompress_bytecode(
            bytecode)
        manifest = AptosBytecodeUtils.decompress_bytecode(
            package.get('manifest'))

        current_parsing_manifest = tomli.loads(manifest)
        parsing_manifest = current_parsing_manifest if parsing_manifest is None else parsing_manifest

        # merge addresses from manifests
        parsing_manifest['addresses'] = {**parsing_manifest.get('addresses', {}), **current_parsing_manifest.get(
            'addresses', {})}
        parsing_manifest['addresses'][current_parsing_manifest['package']
                                      ['name']] = account_address

        # merge dependencies from manifests
        parsing_manifest['dependencies'] = {**parsing_manifest.get('dependencies', {}), **current_parsing_manifest.get(
            'dependencies', {})}

        merge_source_code_string = merge_source_code_string + \
            '\n' + decompressed_source_code

    # build bytecode from source code thats pulled onchain

    try:
        buid_res = await AptosModuleUtils.build_from_template(manifest=tomli_w.dumps(parsing_manifest),
                                                              source_code=merge_source_code_string,
                                                              move_build_path=move_build_path,
                                                              force=False,
                                                              aptos_framework_rev='',
                                                              bytecode_compile_version=params.compile_bytecode_version if params.compile_bytecode_version else '',)
    except verify_exceptions.CanNotBuildModuleException:
        logger.warn(
            "Build with default manifest Move.toml fail, try to replace config [dependencies.AptosFramework] with rev=main.")
        buid_res = await AptosModuleUtils.build_from_template(manifest=manifest,
                                                              source_code=merge_source_code_string,
                                                              move_build_path=move_build_path,
                                                              bytecode_compile_version=params.compile_bytecode_version if params.compile_bytecode_version else '',
                                                              force=True,
                                                              aptos_framework_rev='main')
    if buid_res:
        # get bytecode from build source
        byte_from_source = await AptosBytecodeUtils.extract_bytecode_from_build(
            move_path=move_build_path,
            module_name=module_name
        )
        logger.info(
            "Build and extract bytecode from source code and manifest successfuly. ")
        return byte_from_source
    return None


@config_rule(title='Compare bytecode between published bytecode and published source code onchain')
async def process_compare_bycode(args: VerifyArgs):
    """
    This code will compare bytecode from onchain and source code thats deployed and published onchain
    """
    move_build_path = os.path.join(
        args.move_build_path, f'buiding_{args.account_address}_{int(round(time.time() * 1000))}')
    try:
        bytecode_from_source = await get_bytecode_from_source_code_onchain(move_build_path=move_build_path, params=args)
    except BaseException as e:
        if not args.keep_build_data:
            await AptosModuleUtils.clean_move_build_path(path=move_build_path, delete_folder=True)
        raise e
    bytecode_onchain = await AptosRpcUtils.rpc_account_get_bytecode(params=args)

    bytecode_onchain = AptosBytecodeUtils.clean_prefix(
        bytecode_onchain.get('bytecode'))
    bytecode_from_source = AptosBytecodeUtils.clean_prefix(
        bytecode_from_source)

    logger.debug(f"""
                 Bytecode onchain:
                 {AptosBytecodeUtils.clean_prefix(bytecode_onchain)} 
                 \n\n
                 Bytecode thats build from source onchain:
                 {AptosBytecodeUtils.clean_prefix(bytecode_from_source)}
                 """)

    return bytecode_onchain == bytecode_from_source
