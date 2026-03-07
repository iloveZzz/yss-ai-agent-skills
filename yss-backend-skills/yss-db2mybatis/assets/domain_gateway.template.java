package ${base_package}.domain.${domain_segment}.gateway;

import com.yss.cloud.dto.query.PageQuery;
import com.yss.cloud.dto.result.PageResult;
import ${base_package}.domain.${domain_segment}.model.${domain_name};

import java.util.Optional;

public interface ${domain_name}Gateway {

    ${pk_java_type} create(${domain_name} entity);

    boolean updateById(${domain_name} entity);

    boolean deleteById(${pk_java_type} ${pk_field_name});

    Optional<${domain_name}> findById(${pk_java_type} ${pk_field_name});

    PageResult<${domain_name}> page(PageQuery query);
}
